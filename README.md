# 🚀 Automação de Redes com Temporal, FastAPI e Netbox

Este projeto demonstra uma arquitetura de microsserviços para automação de redes. Ele utiliza **FastAPI** para receber Webhooks do Netbox e o **Temporal.io** para garantir que as tarefas sejam executadas com tolerância a falhas e retentativas automáticas.

## 🏗️ Arquitetura do Projeto

O ambiente é totalmente conteinerizado via Docker e composto por:

* **API Webhook (FastAPI):** Escuta ativamente as requisições HTTP POST (Webhooks do NetBox) na porta `9000``.
* **Temporal Server:** gerencia o estado, as filas de tarefas e garante a resiliência em caso de falhas.
* **Temporal UI:** Interface gráfica web para monitoramento em tempo real do status das automações.
* **Worker (Python/Netmiko):** Microsserviço responsável por consumir a fila do Temporal e executar a configuração final.

## ⚙️ Pré-requisitos

* [Docker](https://www.docker.com/) e Docker Compose instalados.
* [Postman](https://www.postman.com/) para disparar a requisição de teste.

## 🚀 Como rodar o projeto

1. Clone este repositório:
```bash
git clone https://github.com/mayconSouza21/ProjetoTCC.git
```

2. Suba o ambiente com o Docker Compose:
   ```bash
   docker compose up -d --build

3. Verifique se os serviços estão rodando (todos devem estar com status "Up"):
   ```bash
   docker compose ps

## 🧪 Como testar a Resiliência (Demonstração de Falha)

O Worker foi programado com uma **falha intencional de rede** nas primeiras tentativas de execução para demonstrar a política de Retry do Temporal.

1. Dispare uma requisição `POST` para `http://localhost:9000/api/webhook/netbox` com o seguinte JSON no corpo (Body -> raw -> JSON):

```json
{
  "event": "created",
  "model": "vlan",
  "data": {
    "vid": 100,
    "name": "SW_RU",
    "description": "Vlan de teste do TCC"
  }
}
```
2. Acompanhe os logs do Worker em tempo real para ver a falha acontecendo e o sistema aguardando 25 segundos para tentar novamente:
   ```bash
   docker logs -f worker_netmiko

3.Abra a Interface do Temporal no seu navegador:

* URL: http://localhost:8233
