import os
from datetime import date

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from dev_logger.prompts import LOG_FOOTER, SYSTEM_PROMPT
from dev_logger.tools import ALL_TOOLS

load_dotenv()


def build_agent(model: str = "llama-3.3-70b-versatile", local: bool = False):
    if local:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model=model, temperature=0.2)
    else:
        from langchain_groq import ChatGroq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GROQ_API_KEY not found. Copy .env.example to .env and add your key.\n"
                "Get a free key at: https://console.groq.com"
            )
        llm = ChatGroq(model=model, temperature=0.2, api_key=api_key)

    return create_react_agent(model=llm, tools=ALL_TOOLS, prompt=SYSTEM_PROMPT)


def run_agent(repo_path: str, log_date: str = "", local: bool = False, model: str = "llama-3.3-70b-versatile") -> str:
    from dev_logger.tools import init_repo
    init_repo(repo_path)

    target_date = log_date or str(date.today())
    agent = build_agent(model=model, local=local)

    result = agent.invoke({
        "messages": [
            HumanMessage(
                content=f"Analyze the git repository and generate a complete dev log for {target_date}."
            )
        ]
    })

    messages = result.get("messages", [])
    final_message = ""
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
            final_message = msg.content if isinstance(msg.content, str) else str(msg.content)
            break

    return (final_message or "No output generated.") + LOG_FOOTER