import asyncio
import websockets
import sys

async def chat():
    uri = "wss://wowchat.onrender.com/ws"
    async with websockets.connect(uri) as websocket:
        name = input("Enter your name: ")

        async def send():
            while True:
                print("> ", end="", flush=True)
                msg = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                msg = msg.rstrip()
                if msg:
                    await websocket.send(f"{name}: {msg}")

        async def receive():
            while True:
                try:
                    message = await websocket.recv()
                    # Clear current input line, print message, then reprint prompt
                    print(f"\r{message}\n> ", end="", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\nDisconnected.")
                    break

        await asyncio.gather(send(), receive())

asyncio.run(chat())
