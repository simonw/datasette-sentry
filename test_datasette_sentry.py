from datasette_sentry import asgi_wrapper
from datasette.app import Datasette
from datasette import hookimpl
from datasette.plugins import pm
import sentry_sdk
import pytest


def test_asgi_wrapper():
    ds = Datasette(
        metadata={
            "plugins": {"datasette-sentry": {"dsn": "https://demo@sentry.io/1234"}}
        }
    )
    wrapper = asgi_wrapper(ds)
    wrapped = wrapper(ds)
    assert ds == wrapped.app
    assert isinstance(wrapped, sentry_sdk.integrations.asgi.SentryAsgiMiddleware)


def test_not_wrapped_if_no_configuration():
    ds = Datasette()
    wrapper = asgi_wrapper(ds)
    assert ds == wrapper(ds)


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
        response = await ds.client.get("/error")
        assert response.status_code == 500
        if configured:
            assert len(ds._datasette_sentry_events) == 1
        else:
            assert not hasattr(ds, "_datasette_sentry_events")
            assert not hasattr(ds, "_datasette_sentry_envelopes")
    finally:
        pm.unregister(name="undo")
