from app.db.session import SessionLocal
from app.domain.models import Device


def main() -> None:
    db = SessionLocal()
    try:
        if db.query(Device).count() == 0:
            db.add(Device(uid='demo-light-1', ip_address='192.168.1.51', hostname='light1.local', confidence=0.9, metadata_json={'protocol': 'mdns', 'type': 'light'}))
            db.commit()
            print('Seeded demo device')
    finally:
        db.close()


if __name__ == '__main__':
    main()
