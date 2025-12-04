from typing import Any
from agent_framework import ChatMessage, ConcurrentBuilder

async def do_concurrent_workflow(participants: list) -> Any:
    workflow = ConcurrentBuilder().participants(participants).build()

    # Run a prompt through the workflow and print results
    print("🚀 Running prompt through concurrent workflow...\n")
    return await run_prompt_and_print_output(
        workflow,
        "We are launching a new budget-friendly electric bike for urban commuters."
    )


async def run_prompt_and_print_output(workflow, prompt: str) -> None:
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