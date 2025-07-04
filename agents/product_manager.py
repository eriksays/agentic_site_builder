from agents.base import BaseAgent
from typing import Dict
from utils.templates import load_template, format_template


class ProductManagerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            name="ProductManagerAgent",
            input_keys=["user_prompt"],
            output_key="product_spec",
            doc_type="product_spec",
            persona="You are a senior product manager. Based on the user's prompt, create a clear and concise product specification. Include goals, user stories, key features, and success criteria."
        )

    def _generate_response(self, inputs: Dict[str, str], context_docs: Dict[str, str]) -> str:
        template = load_template("product_spec_template.txt")
        # 1️⃣ Pull the original user prompt out of memory
        user_input = context_docs.get("user_input", "")

        # 2️⃣ Flatten every stored doc (including user_input) into one big context
        flattened_context = "\n\n".join(
            f"### {doc_type}\n{text}"
            for doc_type, text in context_docs.items()
        )

        prompt = format_template(
            template,
            persona=self.persona,
            user_prompt=user_input,
            context=flattened_context,
            feedback_section=(
                f"\n\nThe user has provided feedback for improvement:\n{inputs['feedback']}"
                if "feedback" in inputs else ""
            )
        )
        return self.llm.invoke(prompt)