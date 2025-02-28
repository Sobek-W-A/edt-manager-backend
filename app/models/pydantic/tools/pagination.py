"""
Module that provides Pagination for large queries.
"""
from pydantic import BaseModel
from tortoise import Model
from tortoise.queryset import QuerySet


class PydanticPagination(BaseModel):
    """
    Model that helps with pagination.
    """
    page: int = 1
    limit: int = 50
    order_by: str = "id"

    @staticmethod
    def create_model(page: int | None, limit: int | None, order: str | None):
        return PydanticPagination(page=page or 1,
                                  limit=limit or 50,
                                  order_by=order or "id")

    def compute_offset(self) -> int:
        """
        This method computes the offset for the query.
        """
        return (self.page - 1) * self.limit

    async def paginate_query[T: Model](self, query: QuerySet[T]) -> list[T]:
        """
        This method fetches the data from the query provided with pagination.
        The type is generic, but must be a subclass of Model.
        """

        order_field: str = self.order_by.lstrip('-')
        descending: bool = self.order_by.startswith('-')
        if descending:
            return await query.offset(self.compute_offset())\
                              .limit(self.limit).order_by(f'-{order_field}')
        else:
            return await query.offset(self.compute_offset())\
                              .limit(self.limit).order_by(order_field)

    def paginate_list[T: BaseModel](self, query: list[T]) -> list[T]:
        """
        This method paginates a list.
        """
        if self.order_by.startswith('-'):
            key = self.order_by[1:]
            reverse = True
        else:
            key = self.order_by
            reverse = False

        if all(hasattr(item, key) for item in query):
            query.sort(key=lambda x: getattr(x, key), reverse=reverse)

        start = self.compute_offset()
        end = start + self.limit
        return query[start:end]
