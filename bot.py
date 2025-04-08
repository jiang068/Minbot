import asyncio
import hashlib
import os
import shutil
import sys
from pathlib import Path

import nonebot
import time

import uvicorn
from dotenv import load_dotenv
from nonebot.adapters.onebot.v11 import Adapter
import platform
from src.common.logger import get_module_logger

logger = get_module_logger("main_bot")

# 获取没有加载env时的环境变量
env_mask = {key: os.getenv(key) for key in os.environ}

uvicorn_server = None
driver = None
app = None
loop = None

def load_env():
    # 首先加载基础环境变量 .env
    if os.path.exists(".env"):
        load_dotenv(".env", override=True)
        logger.success("成功加载基础环境变量配置")
    else:
        logger.error(".env 文件不存在")
        raise FileNotFoundError(".env 文件不存在")
    
    env = os.getenv("ENVIRONMENT")
    logger.info(f"[load_env] 当前的 ENVIRONMENT 变量值：{env}")
    
def scan_provider(env_config: dict):
    provider = {}

    # 利用未初始化 env 时获取的 env_mask 来对新的环境变量集去重
    # 避免 GPG_KEY 这样的变量干扰检查
    env_config = dict(filter(lambda item: item[0] not in env_mask, env_config.items()))

    # 遍历 env_config 的所有键
    for key in env_config:
        # 检查键是否符合 {provider}_BASE_URL 或 {provider}_KEY 的格式
        if key.endswith("_BASE_URL") or key.endswith("_KEY"):
            # 提取 provider 名称
            provider_name = key.split("_", 1)[0]  # 从左分割一次，取第一部分

            # 初始化 provider 的字典（如果尚未初始化）
            if provider_name not in provider:
                provider[provider_name] = {"url": None, "key": None}

            # 根据键的类型填充 url 或 key
            if key.endswith("_BASE_URL"):
                provider[provider_name]["url"] = env_config[key]
            elif key.endswith("_KEY"):
                provider[provider_name]["key"] = env_config[key]

    # 检查每个 provider 是否同时存在 url 和 key
    for provider_name, config in provider.items():
        if config["url"] is None or config["key"] is None:
            logger.error(f"provider 内容：{config}\nenv_config 内容：{env_config}")
            raise ValueError(f"请检查 '{provider_name}' 提供商配置是否丢失 BASE_URL 或 KEY 环境变量")


async def graceful_shutdown():
    try:
        global uvicorn_server
        if uvicorn_server:
            uvicorn_server.force_exit = True  # 强制退出
            await uvicorn_server.shutdown()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as e:
        logger.error(f"麦麦关闭失败: {e}")


async def uvicorn_main():
    global uvicorn_server
    config = uvicorn.Config(
        app="__main__:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8080)),
        reload=os.getenv("ENVIRONMENT") == "dev",
        timeout_graceful_shutdown=5,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    uvicorn_server = server
    await server.serve()

def raw_main():
    # 利用 TZ 环境变量设定程序工作的时区
    # 仅保证行为一致，不依赖 localtime()，实际对生产环境几乎没有作用
    if platform.system().lower() != "windows":
        time.tzset()

    load_env()

    env_config = {key: os.getenv(key) for key in os.environ}
    scan_provider(env_config)

    # 设置基础配置
    base_config = {
        "websocket_port": int(env_config.get("PORT", 8080)),
        "host": env_config.get("HOST", "127.0.0.1"),
        "log_level": "INFO",
    }

    # 合并配置
    nonebot.init(**base_config, **env_config)

    # 注册适配器
    global driver
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    # 加载插件
    nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    try:
        raw_main()

        app = nonebot.get_asgi()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(uvicorn_main())
        except KeyboardInterrupt:
            logger.warning("收到中断信号，正在优雅关闭...")
            loop.run_until_complete(graceful_shutdown())
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"主程序异常: {str(e)}")
        if loop and not loop.is_closed():
            loop.run_until_complete(graceful_shutdown())
            loop.close()
        sys.exit(1)