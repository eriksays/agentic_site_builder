from agents.base import BaseAgent
from typing import Dict
from utils.templates import load_template, format_template
from utils.context import format_context
from config.settings import ENABLE_PROMPT_LOGGING
from utils.log_utils import log_prompt_and_response
from utils.agent_output import AgentOutput
from datetime import datetime

class GenericAgent(BaseAgent):
    def __init__(self, llm, profile: dict):
        super().__init__(
            llm=llm,
            name=profile["name"],
            input_keys=profile["input_keys"],
            output_key=profile["output_key"],
            doc_type=profile["doc_type"],
            persona=profile["persona"],
            writes_code=profile.get("writes_code", False)
        )
        self.template_file = profile["template_file"]
    
    def _generate_response(self, inputs, context_docs, session_id):
        template = load_template(self.template_file)
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
        response = self.llm.invoke(prompt)
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