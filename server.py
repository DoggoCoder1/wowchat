import asyncio
import os
from websockets import serve
from aiohttp import web

clients = set()
PORT = int(os.environ.get("PORT", 10000))

# WebSocket handler
async def ws_handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            for client in clients:
                if client != ws:
                    await client.send(msg)
    finally:
        clients.remove(ws)

# Health check route for Render
async def healthcheck(request):
    return web.Response(text="OK")

async def start_servers():
    # Start WebSocket server
    ws_server = await serve(ws_handler, "0.0.0.0", PORT)
    print(f"WebSocket server running on port {PORT}")

    # Start HTTP server (on same port)
    app = web.Application()
    app.add_routes([web.get("/", healthcheck)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    # Keep running
    await asyncio.Future()

asyncio.run(start_servers())
