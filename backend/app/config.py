from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SEARXNG_URL: str = "http://localhost:8888"
    SEARXNG_FALLBACKS: str = "https://searx.be,https://search.bus-hit.me"
    REDIS_URL: str = ""
    CORS_ORIGINS: str = "http://localhost:3000"
    PORT: int = 8000

    @property
    def searxng_candidates(self) -> list[str]:
        urls = [self.SEARXNG_URL.strip().rstrip("/")]
        for f in self.SEARXNG_FALLBACKS.split(","):
            f = f.strip().rstrip("/")
            if f and f not in urls:
                urls.append(f)
        return urls

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

settings = Settings()
