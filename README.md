# Minbot

Maibot リポジトリは複雑すぎて扱いにくいため、簡略化しました。

詳細については、ローカライズされたセットアップガイドをご参照ください：

- [中国語版](README_CN.md)
- [英語版](README_EN.md)

# Minbot セットアップガイド

## 1. Python の設定

Python バージョン 3.9 以上がインストールされていることを確認してください。

以下のコマンドで Python のバージョンを確認できます：
```bash
python --version
# または
python3 --version
```
バージョンが 3.9 未満の場合、Python を更新してください。

Python がインストールされていない場合は、以下のコマンドでインストールできます：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3
```

## 2. 環境設定

`venv` を使用して仮想環境を作成することをお勧めします。

以下のコマンドで仮想環境を作成してアクティブ化します：
```bash
python3 -m venv minbot
source minbot/bin/activate  # 環境をアクティブ化
```

仮想環境に入った後、必要な依存関係をインストールします：
```bash
pip install -r requirements.txt
```

## 3. データベース設定

### 方法 1: MongoDB をインストールして起動（ローカル）

- インストールと起動の方法については、[公式 MongoDB ドキュメント](https://www.mongodb.com/docs/manual/installation/) を参照してください。

MongoDB はデフォルトでローカルのポート `27017` に接続します。

### 方法 2: リモート MongoDB リンクを使用

リモートの MongoDB インスタンスを使用する場合、リモート MongoDB サーバーの接続文字列を提供するだけで接続できます。

## 4. NapCat の設定

[公式 NapCat ドキュメント](https://napneko.github.io/) を参照してインストールしてください。

インストールが完了したら、QQ アカウントでログインし、新しい WebSocket サーバーを作成します。逆 WebSocket アドレスを追加します：
```
ws://127.0.0.1:8080/onebot/v11/ws
```

## 5. 設定ファイル

環境設定ファイルを編集します：`.env`

ボットの設定ファイルを編集します：`./config/bot_config.toml`

## 6. ボットの起動

以下のコマンドでボットを起動します：
```bash
python3 bot.py
```
