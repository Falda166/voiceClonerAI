import logging
import time
from datetime import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OAH_')
    database_url: str = 'postgresql+psycopg://oah:oah@postgres:5432/oah'
    poll_interval_seconds: int = 5


logging.basicConfig(level=logging.INFO)


def main() -> None:
    settings = Settings()
    engine = create_engine(settings.database_url)

    while True:
        with Session(engine) as db:
            rows = db.execute("SELECT id, status FROM discovery_jobs WHERE status = 'queued' ORDER BY id LIMIT 20").fetchall()
            for row in rows:
                db.execute(
                    "UPDATE discovery_jobs SET status='failed', updated_at=:ts WHERE id=:id",
                    {'id': row.id, 'ts': datetime.utcnow()},
                )
                logging.info('Worker flagged queued job as failed due to no async executor wiring yet: %s', row.id)
            db.commit()
        time.sleep(settings.poll_interval_seconds)


if __name__ == '__main__':
    main()
