from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

@workflow.defn
class ConfigurarVlanWorkflow:
    @workflow.run
    async def run(self, dados: dict) -> str:
        return await workflow.execute_activity(
            "criar_vlan",
            dados,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=18),
                maximum_interval=timedelta(seconds=18),
                maximum_attempts=2
            )
        )