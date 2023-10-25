#pylint: disable=R0903, E0401, E0611, W0107
"""
It includes schemas to wraps creating, updating, and storing
information from users database.

The schemas included are:

- UserBase    : schema with shared properties
- UserCreate  : schema for receiving user data during the creation of a new user via the API.
- UserUpdate  : schema for receiving user data when updating an existing user via the API.
- UserInDBBase: is the base schema for representing a user in the database,
                and is extended by the UserModel classes.
- UserInDB    : is the schema for representing a user from de database
"""
from typing   import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
        Shared properties
    """
    first_name   : Optional[str]      = None
    second_name  : Optional[str]      = None
    id_number    : Optional[str]      = None
    email        : Optional[EmailStr] = None
    adress       : Optional[str]      = None
    phone_number : Optional[str]      = None


class UserCreate(UserBase):
    """
    Properties to receive via API on creation
    """
    email          : EmailStr
    user_type_id   : int
    hashed_password: Optional[str]
    added_on       : datetime
    added_by       : str


class UserUpdate(UserBase):
    """
    Properties to receive via API on update
    """
    hashed_password: Optional[str]
    changed_on     : Optional[datetime]
    changed_by     : Optional[str]


class UserUpdateForAdmin(UserBase):
    """
    Properties to receive via API on update
    from admin users to employees
    """
    user_type_id: Optional[datetime]
    changed_on  : Optional[datetime]
    changed_by  : Optional[str]


class UserInDBBase(UserBase):
    """
        Base schema for the User information stored in the database

        This model inherits from `UserBase` which contains
        shared properties for the User model, and extends it
        with a unique identifier for each User instance.
        The `Config` inner class sets the behavior of the pydantic model.
    """

    id: Optional[int] = None

    class Config:
        """
        Behaviour of pydantic can be controlled via
        the Config class on a model or a pydantic dataclass

        orm_mode -> whether to allow usage of ORM mode
        """
        orm_mode = True


class User(UserInDBBase):
    """
    Additional properties to return via API
    """
    added_on  : Optional[datetime]
    added_by  : Optional[str]
    changed_on: Optional[datetime]
    changed_by: Optional[str]


class UserInDB(UserInDBBase):
    """
    Additional properties stored in DB
    """
    hashed_password: str
