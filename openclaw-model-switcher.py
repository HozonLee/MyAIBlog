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
            print("使用 'openclaw-model switch list' 查看可用模型")
            sys.exit(1)
        
        if switch_model(config, args.model):
            print("提示：切换模型后需要重启OpenClaw才能生效")
            print("执行 'openclaw-model restart' 重启OpenClaw")
    
    elif args.action == 'restart':
        restart_openclaw()

if __name__ == '__main__':
    main()
