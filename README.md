# datasette-sentry

[![PyPI](https://img.shields.io/pypi/v/datasette-sentry.svg)](https://pypi.org/project/datasette-sentry/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-sentry?include_prereleases&label=changelog)](https://github.com/simonw/datasette-sentry/releases)
[![Tests](https://github.com/simonw/datasette-sentry/workflows/Test/badge.svg)](https://github.com/simonw/datasette-sentry/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sentry/blob/main/LICENSE)

Datasette plugin for configuring Sentry for error reporting
 
## Installation

    pip install datasette-sentry

## Usage

This plugin only takes effect if your `metadata.json` file contains relevant top-level plugin configuration in a `"datasette-sentry"` configuration key.

You will need a Sentry DSN - see their [Getting Started instructions](https://docs.sentry.io/error-reporting/quickstart/?platform=python).

Add it to `metadata.json` like this:

```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": "https://KEY@sentry.io/PROJECTID"
        }
    }
}
```
Settings in `metadata.json` are visible to anyone who visits the `/-/metadata` URL so this is a good place to take advantage of Datasette's [secret configuration values](https://datasette.readthedocs.io/en/stable/plugins.html#secret-configuration-values), in which case your configuration will look more like this:
```json
{
    "plugins": {
        "datasette-sentry": {
            "dsn": {
                "$env": "SENTRY_DSN"
            }
        }
    }
}
```
Then make a `SENTRY_DSN` environment variable available to Datasette.
