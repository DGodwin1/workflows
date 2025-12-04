import asyncio
import os

import orchestrator
import participants

from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.observability import setup_observability



async def main() -> None:
    load_dotenv()
    print("⚙️ Setting up domain agents and concurrent workflow")

    API_KEY = os.getenv("API_KEY")
    ENDPOINT = os.getenv("API_ENDPOINT")
    DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
    WORKFLOW_TYPE = os.getenv("WORKFLOW_TYPE")
    if not API_KEY or not ENDPOINT or not DEPLOYMENT_NAME or not WORKFLOW_TYPE:
        print("☠️ Something isn't set - check API_KEY, API_ENDPOINT, API_DEPLOYMENT_NAME and WORKFLOW_TYPE")
        return

    print("🔭 Setting up observability")
    setup_observability()

    chat_client = AzureOpenAIChatClient(api_key=API_KEY, endpoint=ENDPOINT, deployment_name=DEPLOYMENT_NAME)
    legal, marketer, researcher = participants.create(chat_client)

    o = orchestrator.Orchestrator([legal, marketer, researcher], workflow=WORKFLOW_TYPE)

    await o.do_workflow()

if __name__ == "__main__":
    asyncio.run(main())