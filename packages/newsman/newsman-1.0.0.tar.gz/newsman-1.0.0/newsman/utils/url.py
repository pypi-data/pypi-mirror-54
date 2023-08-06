# -*- coding: utf-8 -*-
PROT_SEP = '://'
HTTP_SCHEME = 'http'
HTTPS_SCHEME = 'https'

class Url:
    """Class for URL objects. Performs sanity checks on URL string and manages
    its components, including scheme, hierarchical domains and extensions.

    Attributes:
        url: Original URL string.
        scheme: HTTP or HTTPS.
        loc: Path of URL.
        domain: Domain of URL.
        ext: The extension of URL resource (if present).
        """

    def __init__(self, url):
        """Object initialization.

        Args:
            url: URL string.
        """

        self.url = url
        self.scheme = self._check_scheme(url)
        self.loc = url.split(PROT_SEP)[1].split('#')[0]

        parts = self.loc.split('/')
        self.domain = parts[0]
        self.ext = self._get_ext(parts)

    def _check_scheme(self, url):
        """Sanity check on URL scheme."""

        if url[:7].lower() == HTTP_SCHEME + PROT_SEP:
            scheme = HTTP_SCHEME
            loc = url[7:]
        elif url[:8].lower() == HTTPS_SCHEME + PROT_SEP:
            scheme = HTTPS_SCHEME
            loc = url[8:]
        else:
            raise ValueError('No scheme or scheme not supported')

        return scheme

    def _get_ext(self, parts):
        """Checks presence of a file extension in url."""

        if len(parts) > 1:
            resource = parts[-1]
            res_parts = resource.split('.')
            if len(res_parts) > 1:
                ext = res_parts[-1]
            else:
                ext = None
        else:
            ext = None

        return ext
