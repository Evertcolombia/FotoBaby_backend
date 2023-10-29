"""
    User repository class
"""
from datetime import datetime
from typing   import List
# local imports
from models.user   import UserModel
from schemas.user  import UserCreate, UserNew, UserUpdate
from crud.user     import CRUDUser
from core.config   import  settings
from core.security import Security


class UserRepo:
    """
    This class represents the repository for managing user entity
    throught the implementation of the UserCrud Interface.

    It acts as a wrapper around a real database or any other storage type.
    """

    def __init__(self) -> None:
        """
        Initializes the UserManufacturerRepo class.

        Args:
            interface (CRUDUser): The CRUD interface for accessing the underlying storage.
        """
        self.interface: CRUDUser = CRUDUser(model=UserModel)
        self.security: Security  = Security()


    async def list_all_users(
        self,
        user_type_id: int | None = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[dict]:
        """
        Retrieves a list of all users, optional
        by user_type_id.

        Returns:
            List[UserModel]: A list of UserModel instances.
        """

        payload = {'user_type_id': user_type_id} if user_type_id else {}
        payload['is_active'] = True

        users   = await self.interface.get_all(
            payload = payload,
            skip    = skip,
            limit   = limit
        )

        return users


    async def get_user_by_id(self, id: int) -> dict:
        """
        Retrieves a user by its ID.

        Args:
            id (int): The ID of the user.

        Returns:
            List[UserModel]: A list containing the UserModel instance.
        """

        user = await self.interface.get_by_id(id=id)
        return user


    async def create_user(
        self, email: str, password: str, user_type_id: int, current_user: str
    ) -> UserNew:
        """
        Create a new user with the provided email, password
        and user_type_id

        Args:
            email (str)      : Email address of the user.
            password (str)   : Password of the user.
            user_type_id(int): user type identifier

        Returns:
            dict: The created user's data.
        """
        user_data = UserCreate(
            email             = email,
            hashed_password   = password,
            user_type_id      = user_type_id,
            added_on          = datetime.now(),
            added_by          = current_user,
            verification_link = None,
        )
        user: UserNew = await self.interface.create(obj_in=user_data)
        return user


    async def update_user(
        self, current_user: str, data: UserUpdate, user_id: int
    ) -> dict:
        """
        Create a new user with the provided email, password
        and user_type_id

        Args:
            email (str)      : Email address of the user.
            password (str)   : Password of the user.
            user_type_id(int): user type identifier

        Returns:
            dict: The created user's data.
        """
        updated_user = await self.interface.update(
            obj_in       = data,
            user_id      = user_id,
            current_user = current_user
        )
        return updated_user


    async def disable_user_account(
        self, *, current_user: str, user_id: int
    ) -> bool:
        """
        Disable a user account by updating its status to inactive.

        Args:
            current_user (str): current user session email.
            user_id (int): user to be deleted.

        Returns:
            bool: True if the user account was successfully disabled;
                False otherwise.
    """
        user_data = UserUpdate(
            changed_by = current_user,
            changed_on = datetime.now(),
            is_active  = False
        )

        disabled = await self.interface.disable_account(
            obj_in  = user_data,
            user_id = user_id
        )
        return disabled

