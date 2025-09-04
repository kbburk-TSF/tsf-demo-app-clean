from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://tsf_user:tsf_pass@db:5432/tsf_demo')
engine = create_engine(DATABASE_URL)
