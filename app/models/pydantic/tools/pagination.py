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

    def compute_offset(self) -> int:
        """
        This method computes the offset for the query.
        """
        return (self.page - 1) * self.limit

    async def paginate_query(self, query: QuerySet[Model] | list[Model]) -> list[Model]:
        """
        This method fetches the data from the query provided with pagination.
        """

        if isinstance(query, QuerySet):
            order_field = self.order_by.lstrip('-')
            descending = self.order_by.startswith('-')

            print("test")

            if descending:
                return await query.offset(self.compute_offset()).limit(self.limit).order_by(f'-{order_field}')
            else:
                return await query.offset(self.compute_offset()).limit(self.limit).order_by(order_field)


        if isinstance(query, list):

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
