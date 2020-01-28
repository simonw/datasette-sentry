from datasette_sentry import asgi_wrapper
import sentry_sdk
import functools


class FakeDatasette:
    def __init__(self, config):
        self.config = config

    def plugin_config(self, name):
        assert "datasette-sentry" == name
        return self.config


def test_asgi_wrapper():
    app = object()
    wrapper = asgi_wrapper(FakeDatasette({"dsn": "https://demo@sentry.io/1234"}))
    wrapped = wrapper(app)
    assert app == wrapped.app
    assert isinstance(wrapped, sentry_sdk.integrations.asgi.SentryAsgiMiddleware)


def test_not_wrapped_if_no_configuration():
    app = object()
    wrapper = asgi_wrapper(FakeDatasette({}))
    assert app == wrapper(app)
