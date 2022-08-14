from datasette import hookimpl
import sentry_sdk


@hookimpl
def startup(datasette):
    config = datasette.plugin_config("datasette-sentry") or {}
    dsn = config.get("dsn")
    if dsn is not None:
        kwargs = dict(dsn=dsn)
        if config.get("capture_events"):
            kwargs["transport"] = CaptureTransport(datasette)
        sentry_sdk.init(**kwargs)


@hookimpl
def handle_exception(exception):
    sentry_sdk.capture_exception(exception)


class CaptureTransport(sentry_sdk.transport.Transport):
    "Transport that captures events in a list, mainly for testing"

    def __init__(self, datasette):
        self.datasette = datasette
        self.datasette._datasette_sentry_events = []
        self.datasette._datasette_sentry_envelopes = []

    def capture_event(self, event):
        self.datasette._datasette_sentry_events.append(event)

    def capture_envelope(self, envelope):
        self.datasette._datasette_sentry_envelopes.append(envelope)
