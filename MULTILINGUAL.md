# Multilingual Support / 多语言支持

## Overview / 概述

Batch File Renamer supports multiple languages to provide a better user experience for users worldwide.

批量文件重命名工具支持多种语言，为全球用户提供更好的使用体验。

## Supported Languages / 支持的语言

- 🇺🇸 **English** 
- 🇨🇳 **中文(简体)** 

## How to Switch Language / 如何切换语言

### Method 1: Command Line / 方法1：命令行

```bash
# English version / 英文版本
python run_i18n.py en

# Chinese version / 中文版本
python run_i18n.py zh

# Auto-detect system language / 自动检测系统语言
python run_i18n.py
```

### Method 2: In-App Switching / 方法2：应用内切换

1. Click the 🌐 button in the toolbar
2. The language will switch between English and Chinese
3. Restart the application to apply changes

点击工具栏中的 🌐 按钮：
1. 语言会在英文和中文之间切换
2. 重启程序以应用更改


## Language Detection / 语言检测

The program automatically detects your system language:
- If system language is Chinese (zh_CN, zh_TW, etc.), uses Chinese
- Otherwise, defaults to English

程序会自动检测系统语言：
- 如果系统语言是中文（zh_CN、zh_TW等），使用中文
- 否则默认使用英文

