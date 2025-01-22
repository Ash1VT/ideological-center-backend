from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import List

__all__ = [
    "RetrieveMixin",
    "RetrieveAllMixin",
    "CreateMixin",
    "UpdateMixin",
    "DeleteMixin"
]

from pydantic import BaseModel

from core.pagination.model import PaginatedModel
from core.pagination.schema import PaginatedOut
from core.uow.generic import GenericUnitOfWork


class RetrieveMixin[Model, RetrieveOut: BaseModel](ABC):
    """
    Mixin class for retrieving instances by ID.

    This mixin provides methods to retrieve instances by their ID using a unit of work and corresponding schemas.

    Attributes:
        schema_retrieve_out (RetrieveOut): The schema for output representation of retrieved instances.
    """

    schema_retrieve_out: RetrieveOut = None

    @abstractmethod
    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> Model:
        """
        Retrieve a database instance by its ID from the repository.

        Args:
            id (int): The ID of the instance to retrieve.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            Model: The retrieved instance.
        """

        raise NotImplementedError

    def get_retrieve_schema(self, instance: Model) -> RetrieveOut:
        """
        Get the output schema for the retrieved instance.

        Args:
            instance (Model): The retrieved instance.

        Returns:
            RetrieveOut: The validated schema for output representation of the retrieved instance.
        """

        return self.schema_retrieve_out.model_validate(instance)

    async def retrieve(self, id: int, uow: GenericUnitOfWork, **kwargs) -> RetrieveOut:
        """
        Retrieve an instance by its ID.

        Args:
            id (int): The ID of the instance to retrieve.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            RetrieveOut: The retrieved instance.
        """

        retrieved_instance = await self.retrieve_instance(id=id, uow=uow, **kwargs)

        return self.get_retrieve_schema(retrieved_instance)


# class RetrieveAllMixin[Model, RetrieveOut: BaseModel](ABC):
#     """
#     Mixin class for listing instances.
#
#     This mixin provides methods to list instances using a unit of work and corresponding schemas.
#
#     Attributes:
#         schema_retrieve_out (RetrieveOut): The schema for output representation of retrieved instances.
#     """
#
#     schema_retrieve_out: RetrieveOut = None
#
#     @abstractmethod
#     async def retrieve_all_instances(self, uow: GenericUnitOfWork, **kwargs) -> List[Model]:
#         """
#         List all database instances from the repository.
#
#         Args:
#             uow (GenericUnitOfWork): The unit of work instance.
#
#         Returns:
#             List[Model]: List of instances.
#         """
#
#         raise NotImplementedError
#
#     def get_list_schema(self, instance_list: List[Model]) -> List[RetrieveOut]:
#         """
#         Get the output schema for the list of instances.
#
#         Args:
#             instance_list (List[Model]): The list of instances.
#
#         Returns:
#             List[RetrieveOut]: List of validated schemas for output representation of instances.
#         """
#
#         return [self.schema_retrieve_out.model_validate(instance) for instance in instance_list]
#
#     async def retrieve_all(self, uow: GenericUnitOfWork, **kwargs) -> List[RetrieveOut]:
#         """
#         List all instances.
#
#         Args:
#             uow (GenericUnitOfWork): The unit of work instance.
#
#         Returns:
#             List[RetrieveOut]: List of instances.
#         """
#
#         instance_list = await self.retrieve_all_instances(uow, **kwargs)
#
#         return self.get_list_schema(instance_list)


class RetrieveAllMixin[Model, RetrieveOut: BaseModel](ABC):
    """
    Mixin class for listing instances.

    This mixin provides methods to list instances using a unit of work and corresponding schemas.

    Attributes:
        schema_retrieve_out (RetrieveOut): The schema for output representation of retrieved instances.
    """

    schema_retrieve_out: RetrieveOut = None
    schema_paginated_out: PaginatedOut[RetrieveOut] = None

    @abstractmethod
    async def retrieve_all_instances(self,
                                     page: int,
                                     per_page: int,
                                     uow: GenericUnitOfWork,
                                     **kwargs) -> PaginatedModel[Model]:
        """
        List all database instances from the repository.

        Args:
            uow (GenericUnitOfWork): The unit of work instance.
            page (int): The page number.
            per_page (int): The number of records per page.

        Returns:
            List[Model]: List of instances.
        """

        raise NotImplementedError

    def get_page_schema(self, paginated_model: PaginatedModel) -> PaginatedOut[RetrieveOut]:
        """
        Get the output schema for the list of instances.

        Args:
            paginated_model (PaginatedModel): The paginated model.

        Returns:
            PaginatedOut: The validated schema for output representation of the paginated model.
        """

        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def retrieve_all(self, uow: GenericUnitOfWork, page: int, per_page: int, **kwargs) -> PaginatedOut[RetrieveOut]:
        """
        List all instances.

        Args:
            uow (GenericUnitOfWork): The unit of work instance.
            page (int): The page number.
            per_page (int): The number of records per page.

        Returns:
            List[RetrieveOut]: List of instances.
        """

        paginated_model = await self.retrieve_all_instances(uow=uow, page=page, per_page=per_page, **kwargs)

        return self.get_page_schema(paginated_model)


class CreateMixin[Model, CreateIn: BaseModel, CreateOut: BaseModel](ABC):
    """
    Mixin class for creating instances.

    This mixin provides methods to create instances using a unit of work and corresponding schemas.

    Attributes:
        schema_create_out (CreateOut): The schema for output representation of created instances.
    """

    schema_create_out: CreateOut = None

    @abstractmethod
    async def create_instance(self, item: CreateIn, uow: GenericUnitOfWork, **kwargs) -> Model:
        """
        Create a new instance in the repository and return created database instance.

        Args:
            item (CreateIn): The instance data to create.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            Model: The created instance.
        """

        raise NotImplementedError

    def get_create_schema(self, instance: Model) -> CreateOut:
        """
        Get the output schema for the created instance.

        Args:
            instance (Model): The created instance.

        Returns:
            CreateOut: The validated schema for output representation of the created instance.
        """

        return self.schema_create_out.model_validate(instance)

    async def create(self, item: CreateIn, uow: GenericUnitOfWork, **kwargs) -> CreateOut:
        """
        Create a new instance and return created serialized instance.

        Args:
            item (CreateIn): The instance data to create.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            CreateOut: The created instance.
        """

        created_instance = await self.create_instance(item=item, uow=uow, **kwargs)

        return self.get_create_schema(created_instance)


class UpdateMixin[Model, UpdateIn: BaseModel, UpdateOut: BaseModel](ABC):
    """
    Mixin class for updating instances.

    This mixin provides methods to update instances using a unit of work and corresponding schemas.

    Attributes:
        schema_update_out (UpdateOut): The schema for output representation of updated instances.
    """

    schema_update_out: UpdateOut = None

    @abstractmethod
    async def update_instance(self, id: int, item: UpdateIn, uow: GenericUnitOfWork,
                              **kwargs) -> Model:
        """
        Update an instance by its ID in the repository and return updated database instance.

        Args:
            id (int): The ID of the instance to update.
            item (UpdateIn): The updated instance data.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            Model: The updated instance.
        """

        raise NotImplementedError

    def get_update_schema(self, instance: Model) -> UpdateOut:
        """
        Get the output schema for the updated instance.

        Args:
            instance (Model): The updated instance.

        Returns:
            UpdateOut: The validated schema for output representation of the updated instance.
        """

        return self.schema_update_out.model_validate(instance)

    async def update(self, id: int, item: UpdateIn, uow: GenericUnitOfWork, **kwargs) -> UpdateOut:
        """
        Update an instance by its ID and return updated serialized instance.

        Args:
            id (int): The ID of the instance to update.
            item (UpdateIn): The updated instance data.
            uow (GenericUnitOfWork): The unit of work instance.

        Returns:
            UpdateOut: The updated instance.
        """

        updated_instance = await self.update_instance(id=id, item=item, uow=uow, **kwargs)

        return self.get_update_schema(updated_instance)


class DeleteMixin[Model](ABC):
    """
    Mixin class for deleting instances.

    This mixin provides methods to delete instances using a unit of work.
    """

    @abstractmethod
    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        """
        Delete an instance by its ID from the repository and return deleted database instance.

        Args:
            id (int): The ID of the instance to delete.
            uow (GenericUnitOfWork): The unit of work instance.
        """

        raise NotImplementedError

    async def delete(self, id: int, uow: GenericUnitOfWork, **kwargs):
        """
        Delete an instance by its ID and return deleted serialized instance.

        Args:
            id (int): The ID of the instance to delete.
            uow (GenericUnitOfWork): The unit of work instance.
        """

        await self.delete_instance(id=id, uow=uow, **kwargs)
