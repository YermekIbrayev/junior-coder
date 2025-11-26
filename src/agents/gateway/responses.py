"""
Response Helpers - Error and response formatting.

Single Responsibility: Response structure creation.
"""


def create_error_response(message: str, error_type: str, code: str) -> dict:
    """
    Create an OpenAI-style error response.

    Args:
        message: Human-readable error message
        error_type: Error type (e.g., "service_unavailable", "invalid_request")
        code: Error code (e.g., "llm_unavailable")

    Returns:
        Dict in OpenAI error format
    """
    return {
        "error": {
            "message": message,
            "type": error_type,
            "code": code
        }
    }


__all__ = ["create_error_response"]
