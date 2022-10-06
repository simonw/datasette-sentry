from datasette.app import Datasette
from datasette import hookimpl
from datasette.plugins import pm
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("configured", (True, False))
async def test_logs_errors_to_sentry(configured):
    class ErrorPlugin:
        __name__ = "ErrorPlugin"

        @hookimpl
        def register_routes(self):
            return (("/error", lambda: 1 / 0),)

    pm.register(ErrorPlugin(), name="undo")
    try:
        # Rest of test goes here
        if configured:
            ds = Datasette(
                metadata={
                    "plugins": {
                        "datasette-sentry": {
                            "dsn": "https://demo@sentry.io/1234",
                            "capture_events": True,
                        }
                    }
                }
            )
        else:
            ds = Datasette()
        await ds.invoke_startup()
        response = await ds.client.get("/error")
        assert response.status_code == 500
        if configured:
            assert len(ds._datasette_sentry_events) == 1
            event = ds._datasette_sentry_events[0]
            assert (
                event["request"].items()
                >= {
                    "method": "GET",
                    "query_string": None,
                    "url": "http://localhost/error",
                }.items()
            )
        else:
            assert not hasattr(ds, "_datasette_sentry_events")
            assert not hasattr(ds, "_datasette_sentry_envelopes")
    finally:
        pm.unregister(name="undo")
