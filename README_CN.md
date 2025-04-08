# Minbot
Maibot 仓库过于复杂且难以处理，因此我进行了简化。  

有关详细信息，请参阅本地化的设置指南：

- [日语版](README_JP.md)
- [英语版](README_EN.md)

# Minbot 安装指南

## 1. Python 配置

确保安装 Python 版本 3.9 或更高版本。

使用以下命令检查您的 Python 版本：
```bash
python --version
# 或者
python3 --version
```
如果版本低于 3.9，请更新 Python。

如果未安装 Python，请使用以下命令安装：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3
```

## 2. 环境配置

我们推荐使用 `venv` 来创建虚拟环境。

使用以下命令创建并激活虚拟环境：
```bash
python3 -m venv minbot
source minbot/bin/activate  # 激活环境
```

进入虚拟环境后，安装所需的依赖：
```bash
pip install -r requirements.txt
```

## 3. 数据库配置

### 方法 1：安装并启动 MongoDB（本地）

- 安装和启动的详细步骤，请参考 [官方 MongoDB 文档](https://www.mongodb.com/docs/manual/installation/)。

MongoDB 默认连接到本地端口 `27017`。

### 方法 2：使用远程 MongoDB 链接

如果您使用的是远程 MongoDB 实例，只需提供远程 MongoDB 服务器的连接字符串。

## 4. NapCat 配置

请参考 [官方 NapCat 文档](https://napneko.github.io/) 进行安装。

安装完成后，使用 QQ 账号登录，创建一个新的 WebSocket 服务器。添加反向 WebSocket 地址：
```
ws://127.0.0.1:8080/onebot/v11/ws
```

## 5. 配置文件

编辑环境配置文件：`.env`

编辑机器人配置文件：`./config/bot_config.toml`

## 6. 启动机器人

使用以下命令启动机器人：
```bash
python3 bot.py
```
