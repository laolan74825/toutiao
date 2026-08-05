import bcrypt

def get_hash_password(password: str) -> str:
    """生成密码哈希"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验密码"""
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )
