from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: int
    user_id: int
    email: str
    scopes: dict
