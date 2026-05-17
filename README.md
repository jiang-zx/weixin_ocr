# weixin_ocr (Local & MCP & Skill Edition)

本项目已全面升级：**移除云端 API 依赖**，接入本地 **PaddleOCR** 引擎，并支持 **MCP Server** 与 **Gemini Skill** 模式。

它可以 100% 准确地识别微信聊天截图文字，并根据气泡颜色精准区分“自己”与“好友”，自动过滤时间、电量和系统提示。

## 特性
- **本地运行**：不花钱、不限流、保护隐私。
- **高精度判定**：结合坐标边界与像素颜色采样（WeChat 绿 vs 白色）。
- **多端支持**：
    - **CLI**: `python main.py`
    - **MCP**: 作为 AI 助手的工具插件使用。
    - **Skill**: 集成到 Gemini CLI。

## 快速开始

### 1. 安装
直接通过 pip 安装（支持自动安装所有依赖）：
```bash
pip install git+https://github.com/jiang-zx/weixin_ocr.git
```

### 2. 本地使用
安装后，你可以在任何地方直接使用命令行：
```bash
weixin-ocr image/test.jpg
```

### 3. 作为 MCP Server 使用
在 Claude/Gemini 配置文件中直接指定命令：
```json
{
  "mcpServers": {
    "weixin-ocr": {
      "command": "weixin-ocr-server"
    }
  }
}
```

## 测试
本项目包含完整的测试套件：
```bash
pytest tests/
```

## 感谢
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 强大的本地 OCR 引擎。
