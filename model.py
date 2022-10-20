from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class Customer(BaseModel):
    name: str
    domain_prefix: str
    username: str
    password: str
    message: str