class BhashaSentryError(Exception):
    """Base exception for BhashaSentry framework."""
    pass

class UnsupportedLanguageError(BhashaSentryError):
    """Raised when an unsupported language code or script is encountered."""
    pass

class RetrievalFailureError(BhashaSentryError):
    """Raised when the retrieval stage fails to return any candidate passages."""
    pass

class ClaimExtractionError(BhashaSentryError):
    """Raised when proposition decomposition fails."""
    pass

class MiscalibrationError(BhashaSentryError):
    """Raised when confidence calibration fails to converge."""
    pass
