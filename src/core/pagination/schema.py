from typing import List

from pydantic import Field, BaseModel


class PaginatedOut[Model: BaseModel](BaseModel):
    page: int = Field(description='Page number of the response')
    per_page: int = Field(description='Number of items per page in the response')
    number_of_pages: int = Field(description='Number of pages in the response')
    total_count: int = Field(description='Total number of items')
    total_filtered_count: int = Field(description='Number of items following given criteria')
    items: List[Model] = Field(description='List of items returned in the response following given criteria')
