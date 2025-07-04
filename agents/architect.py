from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template
from utils.context import format_context
from config.settings import ENABLE_PROMPT_LOGGING
from utils.log_utils import log_prompt_and_response

class ArchitectAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            name="ArchitectAgent",
            input_keys=["product_spec"],
            output_key="architecture_plan",
            doc_type="architecture_plan",
            persona="You are a senior software architect. Based on the product specification, produce a high-level architecture plan. Include major components, technologies, APIs, and any assumptions."
        )

    def _generate_response(self, inputs: Dict[str, str], context_docs: Dict[str, str], session_id: str) -> str:
        template = load_template(f"{self.doc_type}.txt")
        # 1️⃣ Pull the original user prompt out of memory
        #user_input = context_docs.get("user_input", "")

        # 2️⃣ Flatten every stored doc (including user_input) into one big context
        flattened_context = format_context(context_docs)


        prompt = format_template(
            template,
            persona=self.persona,
            context=flattened_context,
            feedback_section=(
                f"\n\nThe user has provided feedback for improvement:\n{inputs['feedback']}"
                if "feedback" in inputs else ""
            )
        )
        # Call the LLM
        response = self.llm.invoke(prompt)
        # Optional logging
        if ENABLE_PROMPT_LOGGING:
            print(f"\n📄 [{self.name}] Prompt from {self.doc_type}")
            print("-" * 80)
            print(prompt)
            print("-" * 80)
            print(f"\n🧠 [{self.name}] LLM Output:")
            print(response)
            print("=" * 80)

            log_prompt_and_response(self.name, session_id, prompt, response)

        return response