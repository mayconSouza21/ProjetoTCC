import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import ConfigurarVlanWorkflow
from activities import criar_vlan

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main():
    while True:
        try:
            c = await Client.connect("temporal_server:7233")

            worker = Worker(
                c,
                task_queue="fila-tarefas-gtic",
                workflows=[ConfigurarVlanWorkflow],
                activities=[criar_vlan]
            )
            logging.info("Worker iniciado com Sandbox ativo e aguardando tarefas...")
            await worker.run()
        except Exception as e:
            logging.warning(f"Aguardando Temporal Server... {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())