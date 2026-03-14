import os
import requests
import logging

logger = logging.getLogger(__name__)

ECHOAPI_BASE = os.getenv("ECHOAPI_BASE_URL", "").rstrip("/")
ECHOAPI_KEY  = os.getenv("ECHOAPI_KEY", "")
_HEADERS     = {"X-API-Key": ECHOAPI_KEY}


def track_view(user_id: int, listing_id: int) -> None:
    """
    EchoAPI does not have a /track-event endpoint yet (Coming Soon on landing page).
    This is a no-op stub — wire it up when the endpoint ships.
    """
    pass


def get_recommendations(user_id: int, limit: int = 4) -> list[dict]:
    """
    Call EchoAPI GET /recommend/?user_id=<id>&limit=<n>
    Returns list of recommendation dicts with keys: id, name, category, score.
    Returns [] on any failure or misconfiguration.
    """
    if not ECHOAPI_BASE or not ECHOAPI_KEY:
        return []
    try:
        res = requests.get(
            f"{ECHOAPI_BASE}/recommend/",
            params={"user_id": user_id, "limit": limit},
            headers=_HEADERS,
            timeout=3,
        )
        if res.ok:
            data = res.json()
            if data.get("success"):
                return data.get("recommendations", [])
    except Exception as e:
        logger.warning(f"EchoAPI error: {e}")
    return []