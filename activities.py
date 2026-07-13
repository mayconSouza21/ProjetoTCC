import asyncio
import logging
from netmiko import ConnectHandler
from temporalio import activity

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@activity.defn
async def criar_vlan(dados: dict) -> str:
    info = activity.info()
    logging.info(f"[Tentativa {info.attempt}] Iniciando provisionamento da VLAN {dados['vid']}...")

    if info.attempt == 1:
        logging.error(f" Simulação de erro na rede na tentativa {info.attempt}!")
        raise ConnectionError("Falha de timeout ao tentar conectar no switch.")

    dispositivo = {
        'device_type': 'linux',
        'host': 'mock_switch',
        'username': 'admin',
        'password': 'admin',
        'port': 2222,
    }

    try:
        def rodar_netmiko():
            with ConnectHandler(**dispositivo) as ssh:
                comandos = [
                    f"echo '=> Criacao da vlan {dados['vid']}'",
                    f"echo '=> Definicao do nome {dados.get('name', 'VLAN')}'"
                ]

                output = ""
                for cmd in comandos:
                    output += ssh.send_command(cmd) + "\n"

                logging.info(f"Output do Switch Simulado:\n{output}")
                ssh.send_command("echo '=> write memory concluido'")
            return "Sucesso"

        loop = asyncio.get_running_loop()
        resultado = await loop.run_in_executor(None, rodar_netmiko)

        logging.info(f" Sucesso! VLAN {dados['vid']} foi criada {info.attempt}.")
        return resultado

    except Exception as e:
        logging.error(f"Erro real de conexão Netmiko: {e}")
        raise e