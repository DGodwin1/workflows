from typing import Any
from agent_framework import ChatMessage, ConcurrentBuilder

"""
// https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/_start-here/step1_executors_and_edges.py
Sample: Concurrent fan-out/fan-in (agent-only API) with default aggregator

Build a high-level concurrent workflow using ConcurrentBuilder and three domain agents.
The default dispatcher fans out the same user prompt to all agents in parallel.
The default aggregator fans in their results and yields output containing
a list[ChatMessage] representing the concatenated conversations from all agents.

Demonstrates:
- Minimal wiring with ConcurrentBuilder().participants([...]).build()
- Fan-out to multiple agents, fan-in aggregation of final ChatMessages
- Workflow completion when idle with no pending work

Prerequisites:
- Azure OpenAI access configured for AzureOpenAIChatClient (use az login + env vars)
- Familiarity with Workflow events (AgentRunEvent, WorkflowOutputEvent)
"""

async def do_concurrent_workflow(participants: list) -> Any:
    # Build a concurrent workflow with the three agents
    workflow = ConcurrentBuilder().participants(participants).build()

    # Run a prompt through the workflow and print results
    print("🚀 Running prompt through concurrent workflow...\n")
    return await run_prompt_and_print_output(
        workflow,
        "We are launching a new budget-friendly electric bike for urban commuters."
    )


async def run_prompt_and_print_output(workflow, prompt: str) -> None:
    """
    Run a prompt through the workflow and pretty-print the final combined messages.

    Args:
        workflow: The concurrent workflow to run
        prompt: The prompt string to process
    """
    events = await workflow.run(prompt)
    outputs = events.get_outputs()

    if outputs:
        print("===== Final Aggregated Conversation (messages) =====")
        for output in outputs:
            messages: list[ChatMessage] | Any = output
            for i, msg in enumerate(messages, start=1):
                name = msg.author_name if msg.author_name else "user"
                print(f"{'-' * 60}\n\n{i:02d} [{name}]:\n{msg.text}")
    else:
        print("No conversations found.")