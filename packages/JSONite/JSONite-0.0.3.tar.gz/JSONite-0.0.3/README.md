# JSONite - The Python-to-Javascript variable transformer for Masonite

This package is intended to be used alongside the [Masonite Framework](https://github.com/MasoniteFramework/masonite) and allows you to pass Python variables to your base template. If no data is passed to the `Javascript` object on a particular request then the object returns an empty string, else it returns a JSON object featuring the passed data.

## Installation:

JSONite can be installed in your Masonite project's home directory with pip:

```bash
pip install JSONite
```

## Setup

After installing JSONite, you'll need to add the `JavascriptProvider` to your application providers in `config/providers.py`.

```python
# config/providers.py

# ...

from jsonite import JavascriptProvider

# ...

PROVIDERS = [
    # ...

    # Third Party Providers
    JavascriptProvider,

    # ...
]

```

After adding the provider, you'll need to add the `JavascripMiddleware` class to `config/middleware.py`.

```python
# config/middleware.py

# ...

from jsonite import JavascriptMiddleware

# ...

HTTP_MIDDLEWARE = [
    # ...
    JavascriptMiddleware,
]

# ...

```

Lastly, you'll want to add the line that actually renders the Javascript in your `base.html` file. By default the function name will be `javascript_data()`, but you can customize this by setting the desired value to the environment variable `JS_TEMPLATE_VAR` in your `.env` file.

```html
<!-- template/base.html -->
<DOCTYPE html>
<html>
    <!-- ... -->
<body>
    <!-- ... -->
    {{ javascript_data() }}
    <!-- ... -->
</body>
</html>
``` 

