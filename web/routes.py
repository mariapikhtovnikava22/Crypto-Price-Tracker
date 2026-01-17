from typing import List

from fastapi import APIRouter

from .api.prices.views import router


all_routers: List[APIRouter] = [router]
