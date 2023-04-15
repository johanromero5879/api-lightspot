from pydantic import Field, BaseModel, validator

from app.common.domain import ValueId, Entity


class BaseAuth(Entity):
    email: str
    password: str


class AuthIn(BaseAuth):
    pass


class AuthOut(BaseAuth):
    id: ValueId = Field(alias="_id")
    password: str | None


class Password(BaseModel):
    password: str = Field(min_length=8, max_length=16)

    @validator('password')
    def password_must_contain_uppercase(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    @validator('password')
    def password_must_contain_lowercase(cls, v):
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

    @validator('password')
    def password_must_contain_digit(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @validator('password')
    def password_must_contain_special_character(cls, v):
        if not any(char in '!@#$%^&*()_-+={}[]|\:;"<>,.?/~`' for char in v):
            raise ValueError('Password must contain at least one special character')
        return v
