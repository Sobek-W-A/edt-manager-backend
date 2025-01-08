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
    page    : int = 1
    limit   : int = 50
    order_by: str = "id"

    def compute_offset(self) -> int:
        """
        This method computes the offset for the query.
        """
        return (self.page - 1) * self.limit

    async def paginate_query(self, query: QuerySet[Model]) -> list[Model]:
        """
        This method fetches the data from the query provided with pagination.
        """
        return await query.offset(self.compute_offset())\
                          .limit(self.limit)\
                          .order_by(self.order_by)
