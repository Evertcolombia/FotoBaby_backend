# pylint: disable=R0903
"""
    This file contains the Base class to be able
    to be used with the other models.
"""
from tortoise        import fields
from tortoise.models import Model


class BaseModel(Model):
    """
    base model for all the other
    models in this backend
    """
    id         = fields.IntField(pk=True)
    added_on   = fields.DatetimeField(auto_now_add=True)
    added_by   = fields.CharField(max_length=255)
    changed_on = fields.DatetimeField(null=True)
    changed_by = fields.CharField(max_length=255, null=True)

    class Meta:
        """
            Specifies that the class is used as a base
            class and a table should not be created in the database for it.
        """
        abstract = True
