import re

def sanitize_json_code_blocks(text: str) -> str:
    """
    Converts triple-quoted code blocks inside JSON into valid escaped strings.
    Only activates if it detects a JSON-like structure with triple-quoted strings.
    """
    # Remove triple quotes around any "content": """ ... """
    # and replace internal newlines with `\n`, escape double quotes
    pattern = re.compile(r'"content"\s*:\s*"""(.*?)"""', re.DOTALL)

    def replacer(match):
        raw_code = match.group(1)
        escaped_code = (
            raw_code.replace('\\', '\\\\')  # escape backslashes
                    .replace('"', '\\"')    # escape quotes
                    .replace('\n', '\\n')   # newline to \n
        )
        return f'"content": "{escaped_code}"'

    return pattern.sub(replacer, text)