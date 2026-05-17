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

### 1. 安装依赖
```bash
pip install -r requestments.txt
```

### 2. 本地测试
```bash
python main.py
```
识别结果将输出到控制台并保存至 `result.txt`。

## 作为 Gemini Skill 使用
本项目自带 `SKILL.md`。在 Gemini CLI 中，只要你进入此项目文件夹，Gemini 就会自动获得“解析微信截图”的能力。

**示例指令：**
> "帮我解析一下 `image/5e5eb526-90e7-4915-8e00-b363f8bce2b2.jpg` 这个截图，总结下我们聊了什么。"

## 作为 MCP Server 使用
在你的 MCP 配置文件（如 `claude_desktop_config.json`）中添加：

```json
{
  "mcpServers": {
    "weixin-ocr": {
      "command": "python",
      "args": ["-u", "/path/to/weixin_ocr/mcp_server.py"]
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
