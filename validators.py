import pydantic
from typing import Optional


class CreateUserValidationModel(pydantic.BaseModel):
    username: pydantic.constr(max_length=50)
    password: pydantic.constr(max_length=100)

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password length must be at least 8 simbols!')
        return value


class PatchUserValidationModel(CreateUserValidationModel):
    username: Optional[pydantic.constr(max_length=50)]
    password: Optional[pydantic.constr(max_length=100)]


class CreateAdvValidationModel(pydantic.BaseModel):
    title: pydantic.constr(max_length=200)
    owner_id: int


class PatchAdvValidationModel(pydantic.BaseModel):
    title: Optional[pydantic.constr(max_length=200)]
    description: Optional[str]
