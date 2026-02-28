---
title: OpenClaw模型切换工具：轻松切换不同大模型
date: 2026-02-28
tags: [OpenClaw, 大模型, 工具, 配置]
---

# OpenClaw模型切换工具：轻松切换不同大模型

## 背景

OpenClaw是一个强大的本地AI助手网关，支持多种大模型。然而，切换不同的大模型通常需要手动编辑配置文件，这对于不熟悉配置的用户来说可能有些复杂。

本文将介绍一个简单的Python工具，帮助你轻松切换OpenClaw使用的大模型，无需手动编辑配置文件。

## 工具功能

- 查看当前使用的模型
- 列出所有可用的模型
- 切换到指定的模型
- 重启OpenClaw以应用更改
- 显示模型切换状态

## 实现代码

```python
#!/usr/bin/env python3
"""
OpenClaw模型切换工具

功能：
- 查看当前使用的模型
- 列出所有可用的模型
- 切换到指定的模型
- 重启OpenClaw以应用更改
- 显示模型切换状态
"""

import json
import os
import subprocess
import sys
import argparse

def get_openclaw_config():
    """获取OpenClaw配置"""
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if not os.path.exists(config_path):
        print(f"错误：找不到OpenClaw配置文件 {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_openclaw_config(config):
    """保存OpenClaw配置"""
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_current_model(config):
    """获取当前使用的模型"""
    if 'model' in config and 'provider' in config['model']:
        provider = config['model']['provider']
        model = config['model'].get('model', 'default')
        return f"{provider}:{model}"
    return "未知模型"

def list_available_models():
    """列出所有可用的模型"""
    models = [
        {"name": "deepseek", "provider": "deepseek", "model": "deepseek-chat"},
        {"name": "qwen", "provider": "qwen", "model": "qwen-turbo"},
        {"name": "minimax", "provider": "minimax", "model": "abab5.5-chat"},
        {"name": "openai", "provider": "openai", "model": "gpt-4o"},
        {"name": "anthropic", "provider": "anthropic", "model": "claude-3-opus-20240229"},
        {"name": "google", "provider": "google", "model": "gemini-1.5-flash"}
    ]
    return models

def switch_model(config, model_name):
    """切换模型"""
    available_models = list_available_models()
    target_model = None
    
    for model in available_models:
        if model['name'] == model_name:
            target_model = model
            break
    
    if not target_model:
        print(f"错误：找不到模型 {model_name}")
        return False
    
    # 更新配置
    if 'model' not in config:
        config['model'] = {}
    
    config['model']['provider'] = target_model['provider']
    config['model']['model'] = target_model['model']
    
    # 保存配置
    save_openclaw_config(config)
    print(f"已切换到模型：{target_model['name']} ({target_model['provider']}:{target_model['model']})")
    return True

def restart_openclaw():
    """重启OpenClaw"""
    print("正在重启OpenClaw...")
    try:
        result = subprocess.run(['openclaw', 'restart'], capture_output=True, text=True)
        if result.returncode == 0:
            print("OpenClaw重启成功！")
            return True
        else:
            print(f"OpenClaw重启失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"执行命令失败：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='OpenClaw模型切换工具')
    parser.add_argument('action', choices=['status', 'list', 'switch', 'restart'],
                        help='操作：status(查看状态), list(列出模型), switch(切换模型), restart(重启)')
    parser.add_argument('model', nargs='?', help='要切换的模型名称')
    
    args = parser.parse_args()
    
    config = get_openclaw_config()
    
    if args.action == 'status':
        current_model = get_current_model(config)
        print(f"当前模型：{current_model}")
    
    elif args.action == 'list':
        print("可用模型列表：")
        models = list_available_models()
        for model in models:
            print(f"  - {model['name']}: {model['provider']}:{model['model']}")
    
    elif args.action == 'switch':
        if not args.model:
            print("错误：请指定要切换的模型名称")
            print("使用 'openclaw-model list' 查看可用模型")
            sys.exit(1)
        
        if switch_model(config, args.model):
            print("提示：切换模型后需要重启OpenClaw才能生效")
            print("执行 'openclaw-model restart' 重启OpenClaw")
    
    elif args.action == 'restart':
        restart_openclaw()

if __name__ == '__main__':
    main()
```

## 使用方法

### 1. 保存工具脚本

将上面的代码保存为 `openclaw-model.py`，并添加执行权限：

```bash
chmod +x openclaw-model.py
```

### 2. 移动到系统路径

将脚本移动到系统路径，方便全局使用：

```bash
sudo mv openclaw-model.py /usr/local/bin/openclaw-model
```

### 3. 查看当前模型

```bash
openclaw-model status
```

### 4. 列出可用模型

```bash
openclaw-model list
```

### 5. 切换模型

```bash
# 切换到DeepSeek模型
openclaw-model switch deepseek

# 切换到Qwen模型
openclaw-model switch qwen

# 切换到OpenAI模型
openclaw-model switch openai
```

### 6. 重启OpenClaw

```bash
openclaw-model restart
```

## 支持的模型

| 模型名称 | 提供商 | 模型ID |
|---------|--------|--------|
| deepseek | deepseek | deepseek-chat |
| qwen | qwen | qwen-turbo |
| minimax | minimax | abab5.5-chat |
| openai | openai | gpt-4o |
| anthropic | anthropic | claude-3-opus-20240229 |
| google | google | gemini-1.5-flash |

## 注意事项

1. 确保OpenClaw已经安装并配置
2. 切换模型后需要重启OpenClaw才能生效
3. 部分模型可能需要API密钥，请确保在OpenClaw配置中正确设置
4. 对于需要OAuth授权的模型（如Qwen），请使用 `openclaw configure` 命令进行授权

## 扩展功能

你可以根据需要扩展这个工具：

1. 添加自定义模型配置
2. 支持模型参数调整
3. 实现模型性能测试
4. 添加模型对比功能

## 总结

这个OpenClaw模型切换工具让你可以轻松管理和切换不同的大模型，无需手动编辑配置文件。通过简单的命令，你可以快速切换到最适合当前任务的模型，提高AI助手的使用效率。

希望这个工具能帮助你更好地使用OpenClaw，享受AI助手带来的便利！