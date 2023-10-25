#pylint: disable=R0903, E0611, W0107
"""
It includes schemas to wraps creating, updating, and storing
information on user types from the database.
The models included are:

- `UserTypeBase`    : defines the shared properties for the country
|                     schema, such as the user_type_name.
- `UserTypeCreate`  : properties to receive via the API on creation
- `UserTypeUpdate`  : properties to receive via the API on update
- `UserTypeInDBBase`: base schema for the user type information stored in the database
- `UserType`        : additional properties to return via the API
- `UserTypeInDB`    : additional properties stored in the database
"""
from typing   import Optional
from pydantic import BaseModel


class UserTypeBase(BaseModel):
    """
    Shared properties
    """
    user_type_name : Optional[str] = None


class UserTypeCreate(UserTypeBase):
    """
    Properties to receive via API on creation
    """
    user_type_name: str


class UserTypeUpdate(UserTypeBase):
    """
    Properties to receive via API on update
    """
    pass


class UserTypeInDBBase(UserTypeBase):
    """
        Base model for the UserType information stored in the database

        This model inherits from `UserTypeBase` which contains
        shared properties for the UserType model, and extends it
        with a unique identifier for each UserType instance.
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


class UserType(UserTypeInDBBase):
    """
    Additional properties to return via API
    """
    pass


class UserTypeInDB(UserTypeInDBBase):
    """
    Additional properties stored in DB
    """
    pass