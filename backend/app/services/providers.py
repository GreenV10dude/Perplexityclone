"""Top-20 BYOK providers — all routed through LiteLLM (OpenAI-compatible)."""
PROVIDERS = [
    {"id": "openai", "label": "OpenAI", "models": ["gpt-4o", "gpt-4o-mini", "o3-mini"], "key_name": "OPENAI_API_KEY", "litellm_prefix": ""},
    {"id": "anthropic", "label": "Anthropic", "models": ["claude-sonnet-4-5", "claude-haiku-4-5", "claude-opus-4-1"], "key_name": "ANTHROPIC_API_KEY", "litellm_prefix": ""},
    {"id": "gemini", "label": "Google Gemini", "models": ["gemini-2.5-pro", "gemini-2.5-flash"], "key_name": "GEMINI_API_KEY", "litellm_prefix": "gemini/"},
    {"id": "xai", "label": "xAI Grok", "models": ["grok-4", "grok-3-mini"], "key_name": "XAI_API_KEY", "litellm_prefix": "xai/"},
    {"id": "deepseek", "label": "DeepSeek", "models": ["deepseek-chat", "deepseek-reasoner"], "key_name": "DEEPSEEK_API_KEY", "litellm_prefix": "deepseek/"},
    {"id": "mistral", "label": "Mistral", "models": ["mistral-large-latest", "mistral-medium-latest"], "key_name": "MISTRAL_API_KEY", "litellm_prefix": "mistral/"},
    {"id": "cohere", "label": "Cohere", "models": ["command-r-plus", "command-r"], "key_name": "COHERE_API_KEY", "litellm_prefix": "command-r-plus"},
    {"id": "groq", "label": "Groq (fast Llama)", "models": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"], "key_name": "GROQ_API_KEY", "litellm_prefix": "groq/"},
    {"id": "together", "label": "Together AI", "models": ["meta-llama/Llama-3.3-70B-Instruct-Turbo"], "key_name": "TOGETHERAI_API_KEY", "litellm_prefix": "together_ai/"},
    {"id": "fireworks", "label": "Fireworks", "models": ["accounts/fireworks/models/llama-v3p3-70b-instruct"], "key_name": "FIREWORKS_API_KEY", "litellm_prefix": "fireworks_ai/"},
    {"id": "openrouter", "label": "OpenRouter (200+ models)", "models": ["openrouter/auto"], "key_name": "OPENROUTER_API_KEY", "litellm_prefix": "openrouter/"},
    {"id": "huggingface", "label": "HuggingFace", "models": ["huggingface/meta-llama/Llama-3.3-70B-Instruct"], "key_name": "HF_TOKEN", "litellm_prefix": "huggingface/"},
    {"id": "qwen", "label": "Alibaba Qwen", "models": ["qwen-max", "qwen-plus"], "key_name": "DASHSCOPE_API_KEY", "litellm_prefix": "dashscope/"},
    {"id": "zhipu", "label": "Zhipu GLM", "models": ["glm-4-plus"], "key_name": "ZHIPU_API_KEY", "litellm_prefix": "zhipuai/"},
    {"id": "moonshot", "label": "Moonshot Kimi", "models": ["moonshot-v1-8k", "kimi-k2-0711-preview"], "key_name": "MOONSHOT_API_KEY", "litellm_prefix": "moonshot/"},
    {"id": "nvidia", "label": "NVIDIA NIM", "models": ["nvidia/llama-3.3-nemotron-super-49b-v1"], "key_name": "NVIDIA_API_KEY", "litellm_prefix": "nvidia_nim/"},
    {"id": "azure", "label": "Azure OpenAI", "models": ["azure/gpt-4o"], "key_name": "AZURE_API_KEY", "litellm_prefix": "azure/"},
    {"id": "bedrock", "label": "AWS Bedrock", "models": ["bedrock/anthropic.claude-sonnet-4-5"], "key_name": "AWS_ACCESS_KEY_ID", "litellm_prefix": "bedrock/"},
    {"id": "vertex", "label": "Vertex AI", "models": ["vertex_ai/gemini-2.5-pro"], "key_name": "VERTEX_PROJECT", "litellm_prefix": "vertex_ai/"},
    {"id": "ollama", "label": "Ollama (local, no key)", "models": ["ollama/llama3.3", "ollama/mistral"], "key_name": "", "litellm_prefix": "ollama/"},
]

PROVIDER_IDS = [p["id"] for p in PROVIDERS]
