# Windsurf-free 账号自动注册助手（同一邮箱无限试用）
# Windsurf-free Account Registration Assistant (Unlimited Trial with One Email)

这是一个自动注册 Windsurf 账号的工具，你只需要一个邮箱即可无限使用windsurfpro用户功能。
This is an automatic registration tool for Windsurf accounts, allowing you to use Windsurf Pro features unlimitedly with just one email.

## 使用前准备
## Prerequisites

1. 下载 Chrome 浏览器便携版
1. Download Chrome Portable Version

   - 下载地址：https://www.google.com/chrome/
   - Download URL: https://www.google.com/chrome/
   - 将下载的 Chrome 文件解压到项目根目录的 `chrome` 文件夹中
   - Extract the downloaded Chrome files to the `chrome` folder in the project root directory

2. 下载 ChromeDriver
2. Download ChromeDriver

   - 下载地址：https://chromedriver.chromium.org/downloads
   - Download URL: https://chromedriver.chromium.org/downloads
   - 确保 ChromeDriver 版本与你的 Chrome 浏览器版本匹配
   - Make sure the ChromeDriver version matches your Chrome browser version
   - 将 chromedriver.exe 放入 `chrome` 文件夹中
   - Place chromedriver.exe in the `chrome` folder

## 原理
## Principle

1. Windsurf、Cursor 新用户赠送试用，区分是否新用户一般使用的是邮箱
Windsurf and Cursor offer free trials for new users, distinguishing new users primarily through email addresses

2. 谷歌邮箱和2925邮箱支持使用邮箱别名功能，即注册一个主邮箱可以使用多个邮箱别名，但最终邮件仍发送到主邮箱，别名格式一般为：用户名+序号@gmail.com，即用户名+001@gmail.com、用户名+002@gmail.com...
Gmail and 2925.com support email aliases, allowing multiple email aliases for one main email address. Emails sent to aliases are delivered to the main inbox. Alias format: username+number@gmail.com (e.g., username+001@gmail.com, username+002@gmail.com...)

3. 把上述2个知识点结合，就是本项目的实现原理
This project combines these two features for implementation

## 实现过程
## Implementation Process

本项目由 Windsurf AI 协助编写代码，主要步骤如下：
This project's code was written with assistance from Windsurf AI, following these steps:

1. 用户选择邮箱（目前支持2925.com和gmail.com）
User selects email provider (currently supports 2925.com and gmail.com)

2. 用户输入用户名和密码，并选择邮箱别名
User inputs username and password, and selects email alias

3. 程序自动执行注册流程
Program automatically executes registration process

4. 创建新的账号后自动登录 Windsurf
Automatically logs into Windsurf after creating new account

5. 试用到期后可继续运行本项目，创建新的用户
Can continue creating new users after trial expiration

## 使用说明
## Usage Instructions

1. 确保已安装 Python 3.8 或更高版本
Ensure Python 3.8 or higher is installed

2. 安装依赖：`pip install -r requirements.txt`
Install dependencies: `pip install -r requirements.txt`

3. 运行程序：`python main.py`
Run the program: `python main.py`

4. 使用新注册的邮箱登录 Windsurf
Use the newly registered email to log in to Windsurf

5. 试用到期后可继续运行本项目，创建新的用户，但你的主邮箱只需要一个
Can continue creating new users after trial expiration, but you only need one main email address

## 免责声明
## Disclaimer

本项目仅供学习和研究使用，请勿用于商业用途。使用本项目产生的任何后果由使用者自行承担。
This project is for learning and research purposes only. Not for commercial use. Users bear all responsibility for any consequences of using this project.
