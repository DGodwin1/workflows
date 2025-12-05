import asyncio
import os

import orchestrator

import dotenv
import agent_framework.observability
import agent_framework.azure



async def main() -> None:
    dotenv.load_dotenv()
    print("⚙️ Setting up domain agents and concurrent workflow")

    API_KEY = os.getenv("API_KEY")
    ENDPOINT = os.getenv("API_ENDPOINT")
    DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
    WORKFLOW_TYPE = os.getenv("WORKFLOW_TYPE")
    if not API_KEY or not ENDPOINT or not DEPLOYMENT_NAME or not WORKFLOW_TYPE:
        print("☠️ Something isn't set - check API_KEY, API_ENDPOINT, DEPLOYMENT_NAME and WORKFLOW_TYPE")
        return

    print("🔭 Setting up observability")
    agent_framework.observability.setup_observability()

    chat_client = agent_framework.azure.AzureOpenAIChatClient(api_key=API_KEY, endpoint=ENDPOINT, deployment_name=DEPLOYMENT_NAME)

    workflow_orchestrator = orchestrator.Orchestrator(chat_client=chat_client, workflow=WORKFLOW_TYPE)

    await workflow_orchestrator.do_workflow()

if __name__ == "__main__":
    asyncio.run(main())