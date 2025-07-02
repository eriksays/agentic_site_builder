from agents.base import BaseAgent
from typing import List

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

    def _generate_response(self, inputs: List[str], context_docs: List[str]) -> str:
        product_spec = inputs[0] if inputs else ""
        context_string = "\n\n".join(context_docs)

        prompt = f"""{self.persona}

        Product Specification:
        {product_spec}

        Prior context:
        {context_string}

        Write a complete high-level architecture plan for the system.
        """

        return self.llm.invoke(prompt)