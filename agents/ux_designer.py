from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template
from utils.context import format_context

class UXDesignerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            name="UXDesignerAgent",
            input_keys=["architecture_plan"],
            output_key="ux_designer_output",
            doc_type="ux_designer_output",
            persona="You are a senior UI designer. Based on the user's prompt, create a visually engaging and consistent user interface plan. Include design goals, component style guidelines, platform-specific considerations (web and mobile), and accessibility compliance suggestions."
        )


    def _generate_response(self, inputs: Dict[str, str], context_docs: List[str]) -> str:
        template = load_template("ux_designer_output.txt")
        
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