class FlashesNotFoundError(Exception):
    def __init__(self):
        message = "Flashes not found"
        super().__init__(message)
