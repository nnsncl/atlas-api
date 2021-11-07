from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash(password: str):
    return password_context.hash(password)
