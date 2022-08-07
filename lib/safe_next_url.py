try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


from flask import request


def safe_next_url(target):
    """ Ensure a URL path is on the same domain as this host. """
    return urljoin(request.host_url, target)