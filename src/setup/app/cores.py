from typing import List

from starlette.middleware.cors import CORSMiddleware


def register_cors(app, origins: List[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
