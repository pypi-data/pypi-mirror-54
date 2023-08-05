# static-thumbnails
Django application providing template tags to create thumbnails from static files using easy-thumbnails

## Installation

```shell script
pip install Pillow easy-thumbnails static-thumbnails
```
## Usage

Add static-thumbnails to your settings.py:
```python
INSTALLED_APPS = [
    # ... regular django apps go here
    'easy_thumbnails',
    'static_thumbnails',
]
```

And then use it as the regular thumbnail tag from easy-thumbnails, but pointing ot to a file in your STATIC_ROOT:

```jinja2
{% static_thumbnail 'some/static/file.png' 150x100 quality=100 HIGH_RESOLUTION as logo %}
<img src="{{ logo.highres_url }}" width="{{ logo.width }}" height="{{ logo.height }}" />
```