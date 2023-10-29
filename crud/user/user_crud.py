# pylint: disable=E0401, W0107, R0903
"""
    crud objects for both user types
"""
from datetime import datetime
from typing import Any, Dict, Generic, List, Type
from crud.base_crud import CRUDBase
from schemas.user   import UserCreate, UserUpdate, UserNew, User
from models.user    import UserModel, UserTypeModel
from core.security  import Security
from core.config    import settings


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
        crud  operations for
        UserModel entities
    """
    def __init__(self, model):
        """intanciate the class entity
            for the user interface

        Args:
            model(UserModel): a reference to UserModel entity
        """
        super().__init__(model=model)
        self.security = Security()


    async def get_all(
        self,
        *,
        payload : Dict[str, Any]       = {},
        skip    : int                  = 0,
        limit   : int                  = 10,
        prefetch: dict[str, UserModel] = None
    ) -> List[dict]:
        """ get a list of users from database

        Args:
            payload (dict): filters to apply on query
            skip (int): from wich row number
            limit (int): to wich row number as limit
            prefect: (dict): to prefetch user relatioships

        Returns:
            list: a list of users from database
        """
        users = await super().get_all(
            payload  = payload,
            skip     = skip,
            limit    = limit,
            prefetch = prefetch
        )

        res_users = self.format_users_res(users_from_pydantic=users)
        return res_users


    async def get_by_id(self, *, id: int) -> dict:
        """get an user from database by it's id

        Args:
            id (int): id of the user to retrieve

        Returns:
            dict with the user attrributes
        """
        user            = await super().get_by_id(id=id)
        serialized_user = await self.model_serializer.from_tortoise_orm(user)

        # five format to return user
        res_user = self.format_users_res(users_from_pydantic=[serialized_user])
        return res_user[0]


    async def create(
        self, *, obj_in: UserCreate
    ) -> UserNew:
        """create a user on database

        Args:
            obj_in (UserCreate): pidantic model
                with the user attributes

        Returns:
            UserNew: created user schema with only required information
        """
        obj_in.hashed_password   = self.security.get_password_hash(password=obj_in.hashed_password)
        obj_in.verification_link = self.security.create_access_token(subject=None)

        # call the parent method to create
        new_user = await super().create(obj_in=obj_in)

        user_schema = UserNew(
            id           = new_user.id,
            email        = new_user.email,
            user_type_id = new_user.user_type.id,
        )
        return user_schema


    async def update(
        self, *, obj_in: UserUpdate, user_id: int, current_user: str
    ) -> dict:
        """ update user properties on database

        Args:
            obj_in (UserUpdate): user data to update
            user_id (int): id of the user to update
            current_user (str): the current user session email

        Returns:
            dict: the updated user as dict
        """
        user = await super().get_by_id(id=user_id)
        if not user:
            print('error not user')

        if not obj_in.changed_on:
            obj_in.changed_on = datetime.now()
        if not obj_in.changed_by:
            obj_in.changed_by = current_user

        updated_user = await super().update(db_obj=user, obj_in=obj_in)
        return updated_user


    async def disable_account(
        self, *, user_id: int, obj_in: UserUpdate
    ) -> bool:
        """ disable user account on database

        Args:
            obj_in (UserUpdate): user data to update
            user_id (int): id of the user to update

        Returns:
            dict: the updated user as dict
        """
        user = await super().get_by_id(id=user_id)
        if not user:
            raise ValueError('User not found')

        await super().update(db_obj=user, obj_in=obj_in)
        return True



    def format_users_res(self, users_from_pydantic):
        """ remove information of a list of users,
        this information will be retrieve to the client
        we need to remove some attributes from the response

        Returns:
            list: users
        """
        res_users = []

        if type(users_from_pydantic) is not list:
            users_from_pydantic = list(users_from_pydantic.__root__)

        for user in users_from_pydantic:
            if type(user) is not dict:
                user = user.dict()

            if user.get('hashed_password'):
                del user['hashed_password']

            del user['user_type']['added_on']
            del user['user_type']['added_by']
            del user['user_type']['changed_on']
            del user['user_type']['changed_by']
            res_users.append(user)

        return res_users
