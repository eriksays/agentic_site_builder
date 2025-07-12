import re

def sanitize_json_code_blocks(text: str) -> str:
    """
    Cleans malformed JSON outputs from LLMs:
    - Removes triple backtick code fences
    - Fixes backtick-wrapped 'content' fields
    - Escapes newlines and quotes inside 'content'
    - Removes trailing commas
    """

    # Remove Markdown-style code fences (```json ... ```)
    text = re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL)

    # Fix backtick-wrapped JavaScript template literals in "content"
    pattern_backtick = re.compile(r'"content"\s*:\s*`(.*?)`', re.DOTALL)
    text = pattern_backtick.sub(lambda m: f'"content": "{escape_json_string(m.group(1))}"', text)

    # Fix triple-double-quote wrapped blocks (rare now)
    pattern_triple_quotes = re.compile(r'"content"\s*:\s*"""(.*?)"""', re.DOTALL)
    text = pattern_triple_quotes.sub(lambda m: f'"content": "{escape_json_string(m.group(1))}"', text)

    # Optional: remove trailing commas (e.g. in final item of a list or object)
    text = re.sub(r",\s*([\]}])", r"\1", text)

    return text

def escape_json_string(s: str) -> str:
    return s.replace('\\', '\\\\') \
            .replace('"', '\\"') \
            .replace('\n', '\\n') \
            .replace('\r', '')  # strip carriage returns just in case

def strip_non_json_prefix(text: str) -> str:
    """
    Strips everything before the first JSON object starting with {"files":
    """
    match = re.search(r'(\{[\s]*"files"\s*:\s*\[)', text)
    if match:
        return text[match.start():]
    return text  # fallback — no valid start found