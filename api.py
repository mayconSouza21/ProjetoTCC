from fastapi import FastAPI, Request
from temporalio.client import Client
import asyncio
from contextlib import asynccontextmanager

client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    while True:
        try:
            client = await Client.connect("temporal_server:7233")
            break
        except Exception:
            await asyncio.sleep(2)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/webhook/netbox")
async def receber_webhook(request: Request):
    data = await request.json()

    if data.get("model") == "vlan" and data.get("event") == "created":
        await client.execute_workflow(
            "ConfigurarVlanWorkflow",
            data["data"],
            id=f"vlan-{data['data']['vid']}",
            task_queue="fila-tarefas-gtic"
        )
        return {"status": "Processo foi iniciado"}

    return {"status": "Processo foi ignorado"}