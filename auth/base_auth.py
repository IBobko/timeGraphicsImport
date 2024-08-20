class BaseAuth:
    def __init__(self):
        self._credentials = None  # Instance variable to store credentials

    def authenticate(self):
        """Attempt to retrieve cached credentials. If not present, perform authentication."""
        if not self._credentials:
            self._credentials = self.perform_authentication()
        return self._credentials

    def perform_authentication(self):
        """Abstract method to perform authentication. Must be implemented by each subclass."""
        raise NotImplementedError(
            "Subclasses must implement this method to handle their specific authentication logic.")
