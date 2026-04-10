from app.core.security import verify_password


def test_password_hash_check() -> None:
    assert verify_password('admin123', '$2b$12$GTu9Fs9ha2Q9YMmJdLx4hOOI6K8hvBvNq4OcNnGfAm8hLkhIwz6mG')
