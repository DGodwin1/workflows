from typing import Any
import agent_framework

class Orchestrator:
    prompt = "We are launching a new budget-friendly electric bike for urban commuters."
    def __init__(self, participants: list, workflow: str) -> None:
        self.participants = participants
        self.pattern = workflow

    async def do_workflow(self):
        print(f"Launching {self.pattern} workflow")
        match self.pattern:
            case "concurrent":
                return await run_prompt_and_print_output(agent_framework.ConcurrentBuilder().participants(self.participants).build(), Orchestrator.prompt)
            case "sequential":
                return await run_prompt_and_print_output(agent_framework.SequentialBuilder().participants(self.participants).build(), Orchestrator.prompt)
            ## case "group_chat": TODO
            case _:
                raise ValueError(f"Unknown workflow pattern: {self.pattern}")

async def run_prompt_and_print_output(workflow, prompt: str) -> None:
    events = await workflow.run(prompt)
    outputs = events.get_outputs()

    if outputs:
        print("===== Final Aggregated Conversation (messages) =====")
        for output in outputs:
            messages: list[agent_framework.ChatMessage] | Any = output
            for i, msg in enumerate(messages, start=1):
                name = msg.author_name if msg.author_name else "user"
                print(f"{'-' * 60}\n\n{i:02d} [{name}]:\n{msg.text}")
    else:
        print("No conversations found.")