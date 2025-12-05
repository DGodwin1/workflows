import asyncio
import os
from contextlib import asynccontextmanager

import dotenv
import fastapi
import prometheus_client
import uvicorn
from fastapi import FastAPI

import agent_framework.azure
import agent_framework.observability
import orchestrator

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔭 Setting up observability")
    agent_framework.observability.setup_observability()
    yield
    print("Bye now 😎")
app = fastapi.FastAPI(debug=False, lifespan=lifespan)

metrics_app = prometheus_client.make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/health")
def health():
    return fastapi.responses.Response(content="OK", media_type="text/plain")

@app.get("/metrics")
def metrics():
    return fastapi.responses.Response(prometheus_client.generate_latest(), media_type=prometheus_client.CONTENT_TYPE_LATEST)

@app.post("/query")
async def query():
    """Endpoint to trigger the workflow"""
    print("⚙️ Setting up domain agents and concurrent workflow")

    API_KEY = os.getenv("API_KEY")
    ENDPOINT = os.getenv("API_ENDPOINT")
    DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
    WORKFLOW_TYPE = os.getenv("WORKFLOW_TYPE")
    if not API_KEY or not ENDPOINT or not DEPLOYMENT_NAME or not WORKFLOW_TYPE:
        print("☠️ Something isn't set - check API_KEY, API_ENDPOINT, DEPLOYMENT_NAME and WORKFLOW_TYPE")
        return fastapi.responses.JSONResponse(
            status_code=500,
            content={"error": "Missing required environment variables"}
        )

    chat_client = agent_framework.azure.AzureOpenAIChatClient(api_key=API_KEY, endpoint=ENDPOINT, deployment_name=DEPLOYMENT_NAME)

    workflow_orchestrator = orchestrator.Orchestrator(chat_client=chat_client, workflow=WORKFLOW_TYPE)

    await workflow_orchestrator.do_workflow()

    return fastapi.responses.JSONResponse(content={"status": "workflow completed"})

if __name__ == "__main__":
    dotenv.load_dotenv()
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
