from datasette import hookimpl
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


@hookimpl
def asgi_wrapper(datasette):
    config = datasette.plugin_config("datasette-sentry") or {}
    dsn = config.get("dsn")
    if dsn is not None:
        sentry_sdk.init(dsn=dsn)

    def wrap_with_class(app):
        if dsn is None:
            return app
        else:
            return SentryAsgiMiddleware(app)

    return wrap_with_class
