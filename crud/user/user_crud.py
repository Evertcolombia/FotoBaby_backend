# pylint: disable=E0401, W0107, R0903
"""
    crud objects for both user types
"""
from crud.base_crud import CRUDBase
from schemas.user   import UserCreate, UserUpdate
from models.user    import UserModel, UserTypeModel
from core      import Security


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
        crud  operations for
        UserModel entities
    """
    async def create(
        self, *, obj_in: UserCreate
    ) -> UserModel:
        """create a user on database

        Args:
            obj_in (UserCreate): pidantic model
                with the user attributes

        Returns:
            UserModel: created user instance
        """
        security: Security = Security()
        # get hashed password
        obj_in.hashed_password = security.get_password_hash(password=obj_in.password)

        # call the parent method to create
        db_obj = await super().create(obj_in=obj_in)
        return db_obj
