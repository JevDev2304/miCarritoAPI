import bcrypt

def hash_password(password: str) -> str:
    """Hashea una contraseña dada en texto plano."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def check_password(plain_password: str, hashed_password_from_db: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con la contraseña hasheada en la base de datos."""
    # Verifica si la contraseña en texto plano coincide con la hasheada almacenada en la base de datos
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password_from_db.encode("utf-8"))
