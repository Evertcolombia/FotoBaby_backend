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


class UserModel(BaseModel):
    """
    represents the user base abstract class.
    for a merchant or a manufacturer
    """
    class Meta:
        """
            Meta class for UserTypeModel
            Defines special attributes for the model,
            such as the database table name.
        """

        table = "users"

    first_name        = fields.CharField(max_length=255, null=True)
    second_name       = fields.CharField(max_length=255, null=True)
    id_number         = fields.CharField(max_length=10, null=True)
    email             = fields.CharField(max_length=50, null=True, unique=True)
    adress            = fields.CharField(max_length=255, null=True)
    phone_number      = fields.CharField(max_length=255, null=True)
    hashed_password   = fields.CharField(max_length=255, null=True)
    is_active         = fields.BooleanField(default=True)
    is_superuser      = fields.BooleanField(default=False)

    # one to many relationship
    # UserTypeModel ->` UserModel`
    user_type = fields.ForeignKeyField(
        "models.UserTypeModel",
        null=True,
        related_name="users"
    )
