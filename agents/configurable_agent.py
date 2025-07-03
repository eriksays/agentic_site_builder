# agents/configurable_agent.py

from agents.base import BaseAgent
from typing import List, Dict
from utils.templates import load_template, format_template
import json
import os

class ConfigurableAgent(BaseAgent):
    def __init__(self, llm, config: Dict):
        super().__init__(
            llm=llm,
            name=config["name"],
            input_keys=config["input_keys"],
            output_key=config["output_key"],
            doc_type=config["doc_type"],
            persona=config["persona"],
            enable_hitl=config.get("hitl", False)
        )
        self.template_file = config["template_file"]

    def _generate_response(self, inputs: Dict[str, str], context_docs: List[str]) -> str:
        template = load_template(self.template_file)
        prompt = format_template(
            template,
            persona=self.persona,
            context="\n\n".join(context_docs),
            feedback_section=(
                f"\n\nThe user has provided feedback for improvement:\n{inputs['feedback']}"
                if "feedback" in inputs else ""
            ),
            **inputs
        )
        return self.llm.invoke(prompt)


def load_agents_from_json(config_dir: str, llm) -> List[BaseAgent]:
    agent_configs = []
    for filename in os.listdir(config_dir):
        if filename.endswith(".json"):
            with open(os.path.join(config_dir, filename), "r") as f:
                config = json.load(f)
                config["filename"] = filename  # useful for debugging
                agent_configs.append(config)

    # ✅ Sort by explicit 'order' key
    sorted_configs = sorted(agent_configs, key=lambda x: x.get("order", 0))

    agents = []
    for config in sorted_configs:
        agent = BaseAgent.from_config(config, llm)
        agents.append(agent)

    return agents