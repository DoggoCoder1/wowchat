import os
import aiohttp
from aiohttp import web

clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                for client in clients:
                    if client is not ws:
                        await client.send_str(msg.data)
    finally:
        clients.remove(ws)

    return ws

async def healthcheck(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", healthcheck)
app.router.add_get("/ws", websocket_handler)

PORT = int(os.environ.get("PORT", 10000))
web.run_app(app, host="0.0.0.0", port=PORT)
