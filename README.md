# WebApp Builder AI

An agentic AI system to scaffold web apps using LangGraph, Ollama, and Chroma.

## Overview

WebApp Builder AI is an agentic workflow framework for rapidly scaffolding and prototyping web applications. It leverages language models (via Ollama), multimodal memory (via ChromaDB), and composable agent flows (via LangGraph) to automate the design, architecture, and code generation of full-stack web apps.

The system organizes your build process into agent "roles" such as Product Manager, Architect, UX Designer, Frontend Developer, and Backend Developer—each guided by expert prompt templates. You can use it in CLI or as a FastAPI web service.

## Features

- **Agentic Workflow:** Each step (spec, architecture, UX, code) is handled by an expert agent.
- **LLM-powered Generation:** Uses Ollama-local or cloud models for planning and code.
- **Chroma Vector Memory:** Persists session context and enables iterative development.
- **Templated Expert Prompts:** Structured output for consistent and high-quality scaffolds.
- **Extensible & Modular:** Add new agents, templates, or swap underlying LLMs.
- **CLI & API:** Run in interactive shell or serve as a FastAPI endpoint.

## Directory Structure

- `agents/` – Core agent implementations (Product Manager, Architect, UX Designer, Frontend, Backend).
- `api/` – FastAPI web server for programmatic access.
- `config/` – Project-wide configuration and settings.
- `llms/` – LLM integration and model selection logic.
- `memory/` – ChromaDB-backed memory and session persistence.
- `templates/` – Prompt and output templates for each agent.
- `utils/` – Utility and helper functions.
- `workflows/` – Orchestration logic for end-to-end flows.
- `app.py` – CLI entry point for interactive scaffolding.

## Installation

1. **Clone the repo:**
   ```sh
   git clone https://github.com/eriksays/agentic_site_builder.git
   cd agentic_site_builder
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **(Optional) Install Ollama & Chroma if not already running.**
   - See [Ollama](https://ollama.com/) and [ChromaDB](https://docs.trychroma.com/) docs.

## Usage

### CLI

Run interactively to start a new project:

```sh
python app.py
```

- You will be prompted for the type of web app and LLM model to use.
- The system will walk through agentic steps: spec → architecture → UX → frontend code → backend code.
- Generated files and output are saved to the `output/` or `generated/` directory.

### API

Run the FastAPI server:

```sh
uvicorn api.server:app --reload
```

Then POST to `/run_workflow/` with your prompt and model.

Example:

```json
{
  "prompt": "A recipe site where users can submit, search, and favorite soup recipes",
  "model_name": "llama3"
}
```

## Contributing

- Fork the repo and submit PRs for new agents, improved templates, or bug fixes.
- Each agent uses a prompt template under `templates/`. Follow the output constraints for each role.
- Tests and CI/CD are welcome!

## Requirements

See [requirements.txt](requirements.txt) for the full list, including:

- `langgraph`, `langchain`, `ollama`, `chroma`, `fastapi`, `uvicorn`, and more.

## License

[MIT](LICENSE) © Erik Says

---

> **Note:** This README is based on code and structure as of July 2025. For the most up-to-date info, view the repo on [GitHub](https://github.com/eriksays/agentic_site_builder).
