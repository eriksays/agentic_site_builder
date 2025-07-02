from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template


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

    def _generate_response(self, inputs: Dict[str, str], context_docs: List[str]) -> str:
        product_spec = inputs.get("product_spec", "")
        feedback = inputs.get("feedback", "")
        context_string = "\n\n".join(context_docs)

        feedback_section = (
            f"\n\nThe user has provided feedback for improvement:\n{feedback}"
            if feedback else ""
        )

        template = load_template("architecture_plan_template.txt")
        prompt = format_template(
            template,
            persona=self.persona,
            product_spec=product_spec,
            context=context_string,
            feedback_section=feedback_section
        )

        return self.llm.invoke(prompt)