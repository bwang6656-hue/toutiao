from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 密码加密
def get_password_hash(password: str):
    return pwd_context.hash(password)

# 密码验证:verify返回True或False
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)