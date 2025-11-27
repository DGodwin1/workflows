import asyncio
import os

import concurrent_orchestration

from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.observability import setup_observability


# Load environment variables from .env file
load_dotenv()

async def main() -> None:
    print("⚙️ Setting up domain agents and concurrent workflow")
    # 1) Create three domain agents using AzureOpenAIChatClient
    API_KEY = os.getenv("API_KEY")
    ENDPOINT = os.getenv("API_ENDPOINT")
    if not API_KEY:
        print("Please set the API_KEY environment variable.")
        return

    print("🔭 Setting up observability")
    setup_observability()

    chat_client = AzureOpenAIChatClient(api_key=API_KEY, endpoint=ENDPOINT, deployment_name="gpt-5-mini", )

    researcher = chat_client.create_agent(
        instructions=(
            "You're an expert market and product researcher. Given a prompt, provide concise, factual insights,"
            " opportunities, and risks."
        ),
        name="researcher",
    )

    marketer = chat_client.create_agent(
        instructions=(
            "You're a creative marketing strategist. Craft compelling value propositions and target messaging"
            " aligned to the prompt."
        ),
        name="marketer",
    )

    legal = chat_client.create_agent(
        instructions=(
            "You're a cautious legal/compliance reviewer. Highlight constraints, disclaimers, and policy concerns"
            " based on the prompt."
        ),
        name="legal",
    )

    await concurrent_orchestration.do_concurrent_workflow([researcher, marketer, legal])


if __name__ == "__main__":
    asyncio.run(main())