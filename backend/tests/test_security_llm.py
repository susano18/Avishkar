
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient
from app.config import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_process_text_overrides_ignored(client: AsyncClient, auth_headers: dict):
    """
    Verify that model and system_prompt overrides are ignored.
    FastAPI will strip unknown fields from the request body if they are not in the schema,
    or at least they won't be in the 'request' object passed to the handler.
    Even if they are passed, our handler now hardcodes the defaults.
    """
    payload = {
        "text": "Hello",
        "model": "expensive-model",
        "system_prompt": "You are a malicious bot."
    }

    with patch("app.api.documents.send_prompt") as mock_send:
        mock_send.return_value = "Mocked response"

        response = await client.post("/api/v1/documents/process-text", json=payload, headers=auth_headers)

        assert response.status_code == 200

        # Verify that send_prompt was called with DEFAULT_MODEL and standard system prompt
        # We need to check kwargs in the lambda or how run_in_executor was called.
        # Actually, if we use positional args in executor, they might not be in kwargs.
        # documents.py calls it like this:
        # await loop.run_in_executor(None, lambda: send_prompt(user_prompt=request.text, system_prompt=system, model=model))
        # Wait, if it's a lambda, then send_prompt is called inside the lambda with keyword args.
        # So mock_send.call_args should have them in kwargs.

        assert mock_send.call_args.kwargs["model"] == settings.DEFAULT_MODEL
        assert mock_send.call_args.kwargs["system_prompt"] == settings.DEFAULT_SYSTEM_PROMPT
        assert mock_send.call_args.kwargs["user_prompt"] == "Hello"

@pytest.mark.asyncio
async def test_filter_run_override_ignored(client: AsyncClient, auth_headers: dict):
    """Verify that model override is ignored in filter run."""
    payload = {
        "syllabus_text": "Syllabus",
        "notes_text": "Notes",
        "model": "expensive-model"
    }

    # Patch the run_filter call in the API module
    with patch("app.api.syllabus_filter.run_filter") as mock_run:
        mock_run.return_value = {
            "identified_topics": "topics",
            "filtered_notes": "notes",
            "formatted_output": "output",
            "processing_time_seconds": 1.0,
            "model_used": settings.DEFAULT_MODEL
        }

        response = await client.post("/api/v1/filter/run", json=payload, headers=auth_headers)

        assert response.status_code == 200
        # Check that run_filter was called with the default model
        assert mock_run.call_args.kwargs["model"] == settings.DEFAULT_MODEL
