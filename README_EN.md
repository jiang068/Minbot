# Minbot
The Maibot repository is too complex and difficult to handle, so I streamlined it.  

For more details, refer to the localized versions of the setup guide:

- [Chinese Version](README_CN.md)
- [Japanese Version](README.md)  

# Minbot Setup Guide

## 1. Python Configuration

Ensure that Python version 3.9 or higher is installed.

Check your Python version with the following command:
```bash
python --version
# or
python3 --version
```
If the version is lower than 3.9, please update Python.

If Python is not installed, install it with:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3
```

## 2. Environment Configuration

We recommend using `venv` to create a virtual environment.

Create and activate the virtual environment with the following commands:
```bash
python3 -m venv minbot
source minbot/bin/activate  # Activate the environment
```

Once inside the virtual environment, install the required dependencies:
```bash
pip install -r requirements.txt
```

## 3. Database Configuration

### Method 1: Install and Start MongoDB (Local)

- For installation and startup, refer to the [Official MongoDB Docs](https://www.mongodb.com/docs/manual/installation/).

MongoDB will connect by default to the local port `27017`.

### Method 2: Using a Remote MongoDB Link

If you are using a remote MongoDB instance, simply provide the connection string for the remote MongoDB server.

## 4. NapCat Configuration

Follow the [Official NapCat Docs](https://napneko.github.io/) for installation.

Once installed, log in with a QQ account and create a new WebSocket server. Add the reverse WebSocket address:
```
ws://127.0.0.1:8080/onebot/v11/ws
```

## 5. Configuration Files

Edit the environment configuration file: `.env`

Edit the bot configuration file: `./config/bot_config.toml`

## 6. Starting the Bot

Run the bot using the following command:
```bash
python3 bot.py
```
