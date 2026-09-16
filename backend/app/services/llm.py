import os
from .providers import PROVIDERS

SYNTHESIZE = """You are a cited answer engine. Use ONLY the provided search results.
Rules:
- Answer directly below the question, concisely, in markdown.
- Every factual claim gets an inline citation like [1], [2] matching SOURCES numbering.
- If results are thin, say so and answer from general knowledge WITHOUT citations for those parts.
- End with a 'Follow-ups:' list of 3 short questions.
"""

def build_context(results: list[dict]) -> str:
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']} ({r['domain']})\nURL: {r['url']}\n{r['snippet']}")
    return "\n\n".join(lines)

def litellm_model(provider_id: str, model: str) -> str:
    p = next((x for x in PROVIDERS if x["id"] == provider_id), None)
    if not p:
        return model
    prefix = p.get("litellm_prefix", "")
    if prefix and not model.startswith(prefix) and "/" not in model:
        # e.g. gemini/ + gemini-2.5-flash ; openrouter/ needs full path from user
        if provider_id in ("openrouter",):
            return model
        return f"{prefix}{model}"
    return model

def apply_byok(provider_id: str, api_key: str, base_url: str = ""):
    """Inject user BYOK key into env for LiteLLM for this request."""
    if not api_key:
        return
    mapping = {
        "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY", "xai": "XAI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY", "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY", "groq": "GROQ_API_KEY",
        "together": "TOGETHERAI_API_KEY", "fireworks": "FIREWORKS_API_KEY",
        "openrouter": "OPENROUTER_API_KEY", "huggingface": "HF_TOKEN",
        "qwen": "DASHSCOPE_API_KEY", "zhipu": "ZHIPU_API_KEY",
        "moonshot": "MOONSHOT_API_KEY", "nvidia": "NVIDIA_API_KEY",
    }
    env_key = mapping.get(provider_id)
    if env_key:
        os.environ[env_key] = api_key
    if base_url:
        os.environ["OPENAI_API_BASE"] = base_url
