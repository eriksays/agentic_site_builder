from agents.base import BaseAgent
from typing import List, Dict
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

    def _generate_response(self, inputs: Dict[str, str], context_docs: List[str]) -> str:
        template = load_template("product_spec_template.txt")
        prompt = format_template(
            template,
            persona=self.persona,
            user_prompt=inputs.get("user_prompt", ""),
            context="\n\n".join(context_docs),
            feedback_section=(
                f"\n\nThe user has provided feedback for improvement:\n{inputs['feedback']}"
                if "feedback" in inputs else ""
            )
        )
        return self.llm.invoke(prompt)