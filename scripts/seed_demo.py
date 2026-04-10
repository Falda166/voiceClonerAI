from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.models.entities import Device

engine = create_engine('postgresql+psycopg://oah:oah@localhost:5432/oah')

with Session(engine) as db:
    db.add(Device(stable_key='demo-kitchen-sensor', ip_address='192.168.1.22', protocol='mdns', confidence=85))
    db.commit()
print('seeded')
