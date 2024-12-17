# Windsurf VIP 账号注册工具

这是一个自动化的 Windsurf VIP 账号注册工具，可以帮助你快速注册账号并获取 VIP 功能。

## 运行要求

### Chrome 浏览器

你有两种方式来配置 Chrome 浏览器：

1. **使用便携版 Chrome**（推荐）
   - 下载 Chrome 便携版
   - 将解压后的文件夹重命名为 `chrome`
   - 将整个 `chrome` 文件夹放入程序运行目录
   - 确保 `chrome` 文件夹中包含 `chrome.exe`

2. **使用系统安装的 Chrome**
   - 从 [Chrome 官网](https://www.google.com/chrome/) 下载并安装 Chrome 浏览器
   - 程序会自动检测系统中已安装的 Chrome

### ChromeDriver

你同样有两种方式来配置 ChromeDriver：

1. **放置在程序目录**（推荐）
   - 从 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载与你的 Chrome 版本匹配的 ChromeDriver
   - 将 `chromedriver.exe` 放入程序运行目录的 `chrome` 文件夹中

2. **使用系统中的 ChromeDriver**
   - 确保 ChromeDriver 已添加到系统环境变量中
   - 版本必须与 Chrome 浏览器版本匹配

## 目录结构

程序运行目录应该包含以下文件和文件夹：

```
windsurf-vip-free/
├── chrome/                  # Chrome 相关文件夹
│   ├── chrome.exe          # Chrome 便携版（可选）
│   └── chromedriver.exe    # ChromeDriver（推荐放在这里）
└── windsurf-vip-free.exe   # 主程序
```

## 常见问题

1. **提示找不到 Chrome**
   - 检查是否已安装 Chrome 或正确放置便携版 Chrome
   - 如果使用便携版，确保 `chrome.exe` 位于 `chrome` 文件夹中
   - 如果使用系统安装版，确保 Chrome 已正确安装

2. **提示找不到 ChromeDriver**
   - 确保 ChromeDriver 版本与 Chrome 版本匹配
   - 检查 ChromeDriver 是否正确放置在 `chrome` 文件夹中

3. **Chrome 版本与 ChromeDriver 不匹配**
   - 访问 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载对应版本的 ChromeDriver
   - 将新的 ChromeDriver 放入 `chrome` 文件夹中

## 注意事项

- 建议使用便携版 Chrome 和本地 ChromeDriver，这样可以确保版本匹配和稳定性
- 程序首次运行时会自动创建必要的文件夹
- 如果遇到问题，程序会自动打开相关下载页面引导你完成安装

## 技术支持

如果遇到问题，请查看程序目录下的 `error.log` 文件了解详细错误信息。
