from dependency_injector import containers, providers

from app.infrastructure.integrations.deribit import DeribitClient
from app.infrastructure.repositories.price_repository import PricesRepository
from app.infrastructure.uow.prices_unit_of_work import PricesUnitOfWork
from app.services.fetch_prices_service import FetchPricesService
from helpers.db_config import get_async_scoped_session
from settings.deribit import DerbitConfig


class FetchPricesContainer(containers.DeclarativeContainer):

    async_session = providers.Resource(get_async_scoped_session)

    deribit_client = providers.Factory(DeribitClient)

    prices_repository = providers.Factory(PricesRepository, session=async_session)

    prices_uow = providers.Factory(PricesUnitOfWork, prices_repo=prices_repository, session=async_session)

    fetch_prices_service = providers.Factory(
        FetchPricesService,
        client=deribit_client,
        prices_uow=prices_uow,
        tickers=DerbitConfig.TICKERS,
    )
