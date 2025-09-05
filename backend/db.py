from sqlalchemy import create_engine
import os

raw_url = os.getenv("DATABASE_URL", "postgresql://tsf_user:tsf_pass@localhost:5432/tsf_demo")
# Many managed Postgres (including Railway) require SSL. Add it if missing.
if "sslmode=" not in raw_url:
    separator = "&" if "?" in raw_url else "?"
    raw_url = f"{raw_url}{separator}sslmode=require"

engine = create_engine(raw_url, pool_pre_ping=True)
