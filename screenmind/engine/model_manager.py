"""
Model Manager for ScreenMind

NOTE: This module has been deprecated. The LLM backend now uses a custom API endpoint
configured via LLM_API_BASE_URL, LLM_API_KEY, and LLM_MODEL_NAME environment variables.

This file is kept for backward compatibility only. All model management (download, server
lifecycle) functions are no-op stubs.
"""

import logging
from typing import Optional

from screenmind.config import settings

logger = logging.getLogger("screenmind.engine.model_manager")


# Stub model info - kept for API compatibility
AVAILABLE_MODELS = []


def get_model_info(key: str) -> Optional[dict]:
    """Get model metadata by key (stub)."""
    return None


def is_audio_capable(key: Optional[str] = None) -> bool:
    """Check if the given (or active) model supports audio input (stub)."""
    return False


def get_active_capabilities() -> dict:
    """Get capability flags for the active model (stub)."""
    return {"audio": False, "vision": True}  # Vision supported via base64 images


def list_models() -> list:
    """List all available models (stub)."""
    return []


def is_model_downloaded(key: str) -> bool:
    """Check if a model is downloaded (stub)."""
    return True  # Assume model is available via API


def start_server(model_key: Optional[str] = None, timeout: int = 60) -> bool:
    """Start server (no-op stub - using external API)."""
    logger.info("start_server called but using external LLM API - no local server needed")
    return True


def stop_server():
    """Stop server (no-op stub)."""
    pass


def switch_model(key: str) -> bool:
    """Switch model (no-op stub - model configured via LLM_MODEL_NAME)."""
    logger.warning(f"switch_model({key}) called but model is configured via LLM_MODEL_NAME env var")
    return True


def restart_server() -> bool:
    """Restart server (no-op stub)."""
    return True


def get_active_model() -> Optional[str]:
    """Get the currently active model key."""
    return settings.llm_model_name


def is_server_running() -> bool:
    """Check if server process is alive (stub - always True if API reachable)."""
    from screenmind.engine import llm_client
    return llm_client.is_available()


def get_model_status() -> dict:
    """Get the full model status for the frontend."""
    from screenmind.engine import llm_client
    
    if llm_client.is_available():
        return {
            "status": "ready",
            "active_model": settings.llm_model_name,
            "model_downloaded": True,
            "capabilities": {"audio": False, "vision": True},
            "download": None,
        }
    else:
        return {
            "status": "error",
            "active_model": settings.llm_model_name,
            "model_downloaded": False,
            "capabilities": {"audio": False, "vision": True},
            "download": None,
            "message": "Cannot connect to LLM API endpoint. Check LLM_API_BASE_URL configuration.",
        }


def download_and_start(key: str) -> bool:
    """Download and start model (no-op stub)."""
    logger.error("download_and_start called but using external LLM API - this function is not available")
    return False


def cancel_download() -> bool:
    """Cancel download (no-op stub)."""
    return False


def get_download_state() -> dict:
    """Get download state (stub)."""
    return {
        "active": False,
        "model": None,
        "status": "idle",
        "downloaded_bytes": 0,
        "message": "",
    }
