"""
    Module that contains the definition of the environment enumerators used in the application.
"""
from enum import Enum

class Environments(str, Enum):
    """
    Environment stages
    """
    PRODUCTION = '.env.prod'
    UAT        = '.env.uat'
    DEVELOP    = '.env.dev'
    TEST       = '.env.test'


class UserTypesEnum(str, Enum):
    """
    User's types
    """
    SUPERADMIN = 1
    ADMIN      = 2
    SELLER     = 3
