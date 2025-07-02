from agents.base import BaseAgent
from typing import List

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

    def _generate_response(self, inputs: List[str], context_docs: List[str]) -> str:
        user_prompt = inputs[0] if inputs else ""
        context_string = "\n\n".join(context_docs)

        prompt = f"""{self.persona}

        User prompt:
        {user_prompt}

        Previous context:
        {context_string}

        Please write a full product specification below.
        """

        return self.llm.invoke(prompt)