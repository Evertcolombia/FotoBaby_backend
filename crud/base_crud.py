# pylint: disable=C0114, E0401, C0115, C0116, W0102, W0622, W0611
from typing                         import Any, Dict, Generic, List, Type
from tortoise.query_utils           import Prefetch
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.queryset              import QuerySet
from tortoise.contrib.pydantic      import pydantic_model_creator, pydantic_queryset_creator
# local imports
from schemas.general                import CreateSchemaType, ModelType, UpdateSchemaType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
        Base class for CRUD operations.
    """

    def __init__(
        self, *,
        model : Type[ModelType]
    ) -> None:
        """
        Initializes the CRUDBase class.
        """
        self.model : ModelType = model
        self.model_serializer = pydantic_model_creator(self.model)
        self.model_list_serializer = pydantic_queryset_creator(self.model)


    async def get_all(
        self,
        *,
        payload : Dict[str, Any]       = {},
        skip    : int                  = 0,
        limit   : int                  = 10,
        prefetch: dict[str, ModelType] = None
    ) -> List[PydanticModel]:
        """Retrieve a list of objects based on the provided filter.

        Args:
            payload (Dict[str, Any], optional): The filter parameters as a dictionary.
            skip (int, optional)              : The number of records to skip. Defaults to 0.
            limit (int, optional)             : The maximum number of records to return. Defaults to 10.

        Returns:
            List[PydanticModel]: A list of Obj-Tortoise objects matching the filter.
        """

        query: QuerySet = self.model.filter(**payload).offset(skip).limit(limit)

        if prefetch:
            for column_name, model_name in prefetch.items():
                query = query.prefetch_related(
                    Prefetch(column_name, queryset=model_name.all())
                )

        objs = await self.model_list_serializer.from_queryset(query.all())
        return objs



    async def create(self, *, obj_in: CreateSchemaType) -> PydanticModel:
        """Create a new object with the provided data.

        Args:
            obj_in (CreateSchemaType): The data to create the new object.

        Returns:
            PydanticModel: The created Obj-Tortoise object.
        """

        obj: ModelType = await self.model.create(**obj_in.dict())
        serialized_obj = await self.model_serializer.from_tortoise_orm(obj)
        return serialized_obj


    async def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> PydanticModel:
        """Update an existing object with the provided data.

        Args:
            db_obj (ModelType)       : The existing Tortoise model object to update.
            obj_in (UpdateSchemaType): The data to update the object.

        Returns:
            PydanticModel: The updated Obj-Tortoise representation of the object.
        """

        # update the object in the db
        await db_obj.update_from_dict(obj_in.dict(exclude_unset=True)).save()

        # get the updated object
        updated_obj = await self.get_by_id(id=db_obj.id)
        return updated_obj


    async def delete(self, *, db_obj: ModelType) -> int:
        """Delete an existing object.

        Args:
            db_obj (ModelType): The existing Tortoise model object to delete.

        Returns:
            int: The number of deleted objects (0 or 1).
        """

        delete: int = await db_obj.delete()
        return delete

    async def get_by_id(self, *, id: int) -> PydanticModel:
        """Retrieve an object by its ID.

        Args:
            id (int): The ID of the object to retrieve.

        Returns:
            PydanticModel: The Object-Tortoise representation of the retrieved object.
        """

        obj = await self.model.get_or_none(id=id)
        return obj

    async def count(self, *, payload: Dict[str, Any] = {}) -> int:
        """Count the number of objects based on the provided filter.

        Args:
            payload (Dict[str, Any], optional): The filter parameters as a dictionary.

        Returns:
            int: The total count of objects matching the filter.
        """

        count : int = await self.model.filter(**payload).all().count()
        return count
