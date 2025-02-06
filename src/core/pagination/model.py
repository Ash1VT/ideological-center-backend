from dataclasses import dataclass
from typing import List


@dataclass
class PaginatedModel[Model]:
    page: int
    per_page: int
    number_of_pages: int
    total_count: int
    total_filtered_count: int
    items: List[Model]
