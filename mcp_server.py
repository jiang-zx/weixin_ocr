import asyncio
import os
import argparse
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
import mcp.types as types
from main import process_image

server = Server("wechat-ocr-parser")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="parse_wechat_screenshot",
            description="解析微信聊天截图，识别文字并根据气泡颜色区分好友和自己，返回对话记录 (Markdown 格式)。",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "本地微信截图文件的绝对路径。"
                    }
                },
                "required": ["image_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name != "parse_wechat_screenshot":
        raise ValueError(f"未知的工具名称: {name}")
        
    image_path = arguments.get("image_path")
    if not image_path:
        return [types.TextContent(type="text", text="错误: 未提供 image_path")]
    
    # Resolve relative path if necessary
    if not os.path.isabs(image_path):
        image_path = os.path.abspath(image_path)
        
    if not os.path.exists(image_path):
        return [types.TextContent(type="text", text=f"错误: 找不到文件 {image_path}")]
        
    try:
        dialogues = process_image(image_path)
        transcript = "\n".join(dialogues)
        if not transcript:
            transcript = "未识别到任何对话内容。"
        return [types.TextContent(type="text", text=transcript)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"处理图像时发生错误: {str(e)}")]

async def run_stdio():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(
            server_name="wechat-ocr",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=types.ServerCapabilities(
                    tools={}
                )
            )
        ))

def run_sse(host="0.0.0.0", port=8000):
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route
    import uvicorn

    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
            await server.run(read_stream, write_stream, InitializationOptions(
                server_name="wechat-ocr",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=types.ServerCapabilities(
                        tools={}
                    )
                )
            ))

    app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=sse.handle_post, methods=["POST"]),
        ],
    )

    print(f"MCP SSE Server starting at http://{host}:{port}/sse")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WeChat OCR MCP Server")
    parser.add_argument("--mode", choices=["stdio", "sse"], default="stdio", help="Run mode (default: stdio)")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE mode (default: 8000)")
    args = parser.parse_args()

    if args.mode == "sse":
        run_sse(port=args.port)
    else:
        asyncio.run(run_stdio())
