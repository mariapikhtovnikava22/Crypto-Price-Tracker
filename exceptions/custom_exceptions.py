class BaseAppError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PriceNotFoundError(BaseAppError):
    def __init__(self, message: str = "Price not found"):
        super().__init__(message)
