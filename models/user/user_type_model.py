#pylint: disable=R0903, C0303, E0401
"""
Module: models

This module contains the models used in the application.
It defines the structure of the database tables
using Tortoise ORM and models defined with the `BaseModel` class.

- `UserModel`             : representing the user table.
- `UserRatingModel`       : representing the user rating table.
- `UserTypeModel`         : representing the user type table.
- `ContactsModel`         : representing the user contact table.

"""
from tortoise          import fields
# BaseModel
from models.base_model import BaseModel


class UserTypeModel(BaseModel):
    """
    represents the user_type table.
    Each row on this table represents a
    diffrent user_type entity for the app
    """
    class Meta:
        """
            Meta class for UserTypeModel
            Defines special attributes for the model,
            such as the database table name.
        """

        table = "user_type"

    user_type_name = fields.CharField(max_length=255)
    users = fields.ReverseRelation["UserModel"]
