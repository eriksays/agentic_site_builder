import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../templates")

def load_template(name: str) -> str:
    path = os.path.join(TEMPLATE_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def format_template(template: str, **kwargs) -> str:
    return template.format(**kwargs)