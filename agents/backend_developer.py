from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template
from utils.context import format_context
from config.settings import ENABLE_PROMPT_LOGGING
from utils.log_utils import log_prompt_and_response

class BackEndDeveloperAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            name="BackEndDeveloperAgent",
            input_keys=["frontend_developer"],
            output_key="backend_developer_output",
            doc_type="backend_developer",
            persona = (
                "You are a senior backend developer. Based on the product spec and architecture, implement the backend API "
                "using a modern Python framework such as FastAPI. Include route handlers, data models, and necessary config files. "
                "Structure your code into modular files. Return a list of code files with their relative paths and contents."
            )
        )


    def _generate_response(self, inputs: Dict[str, str], context_docs: List[str], session_id: str) -> str:
        template = load_template(f"{self.doc_type}.txt")
        
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