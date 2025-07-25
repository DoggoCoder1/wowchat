import asyncio
import os
from aiohttp import web
import websockets

clients = set()

# PORT for Render health check
HTTP_PORT = int(os.environ.get("PORT", 10000))
# Fixed port for WebSocket server
WS_PORT = 8765

# WebSocket handler
async def ws_handler(websocket):
    clients.add(websocket)
    try:
        async for msg in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(msg)
    finally:
        clients.remove(websocket)

# HTTP server handler (used only for Render's health check)
async def handle_healthcheck(request):
    return web.Response(text="OK")

async def main():
    # Start dummy HTTP server
    app = web.Application()
    app.router.add_get("/", handle_healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", HTTP_PORT)
    await site.start()
    print(f"HTTP server running on port {HTTP_PORT} (for health checks)")

    # Start WebSocket server
    await websockets.serve(ws_handler, "0.0.0.0", WS_PORT)
    print(f"WebSocket server running on port {WS_PORT}")

    await asyncio.Future()  # Run forever

asyncio.run(main())
