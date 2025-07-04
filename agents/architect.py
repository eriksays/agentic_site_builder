from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template
from utils.context import format_context


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

    def _generate_response(self, inputs: Dict[str, str], context_docs: Dict[str, str]) -> str:
        template = load_template("architecture_plan_template.txt")
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
        return self.llm.invoke(prompt)