from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # specify bcrypt hashing algorithm

def hash_password(password: str):
    return pwd_context.hash(password)
