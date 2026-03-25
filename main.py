#main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Load frontend
with open("templates/index.html") as f:
    html = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)