# Flake8-Flask

![Build Status](https://travis-ci.org/pgjones/flake8-flask.png?branch=master)

Flake8-Flask is a [flake8](http://flake8.readthedocs.org/en/latest/)
plugin that checks flask against some opinionated styles. Notably
checking for trailing slashes in routes, that routes do not have
multiple methods and that blueprint prefixes match a specified form.

## Warnings

This package adds 3 new flake8 warnings
 - `F440`: Route is Missing Trailing Slash.
 - `F441`: Route has more than 1 method.
 - `F450`: Blueprint prefix does not match /v\d+.

## Limitations

Any decorator added in the format

```python
@app.route(path, methods=[])
```

is considered a route regardless of the name or type of app. The path
and methods are then checked.

Any call in the format

```python
app.register_blueprint(blueprint, url_prefix=prefix)
```

is considered a blueprint registration regardless of the name or type
of app. The prefix is then checked.
