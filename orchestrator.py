from typing import Any

import agent_framework

class Orchestrator:
    prompt = "We are launching a new budget-friendly electric bike for urban commuters."
    def __init__(self, chat_client, workflow: str) -> None:
        self.chat_client = chat_client
        self.pattern = workflow
        self.participants = self._create_participants(self.chat_client)

    async def do_workflow(self):
        print(f"Launching {self.pattern} workflow")
        match self.pattern:
            case "concurrent":
                return await self._run_prompt_and_print_output(agent_framework.ConcurrentBuilder().participants(self.participants).build(), Orchestrator.prompt)
            case "sequential":
                return await self._run_prompt_and_print_output(agent_framework.SequentialBuilder().participants(self.participants).build(), Orchestrator.prompt)
            ## case "group_chat": TODO
            case _:
                raise ValueError(f"Unknown workflow pattern: {self.pattern}")

    async def _run_prompt_and_print_output(self, workflow, prompt: str) -> None:
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

    def _create_participants(self, chat_client) -> list:
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
        return [legal, marketer, researcher]



