"""Helpers for returning absolute media URLs from serializers."""


def media_url(request, file_field):
    """Absolute URL for ``file_field`` (or ``None``).

    Uses the request to build a host-correct URL instead of a hard-coded
    ``127.0.0.1:8000`` base, so responses are valid in every environment.
    """
    if not file_field:
        return None
    url = file_field.url
    if request is not None:
        return request.build_absolute_uri(url)
    return url
