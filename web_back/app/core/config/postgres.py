from typing import Optional

class PostgresConfig:
    db: Optional[str] = None
    host: str = "127.0.0.1"
    port: str = "5432"
