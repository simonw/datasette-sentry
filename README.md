# datasette-sentry

[![PyPI](https://img.shields.io/pypi/v/datasette-sentry.svg)](https://pypi.org/project/datasette-sentry/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-sentry.svg?style=svg)](https://circleci.com/gh/simonw/datasette-sentry)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-sentry/blob/master/LICENSE)

Datasette plugin for configuring Sentry for error reporting.

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
