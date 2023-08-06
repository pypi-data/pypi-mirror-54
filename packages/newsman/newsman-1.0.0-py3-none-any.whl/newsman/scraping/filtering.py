# -*- coding: utf-8 -*-

class UrlFilter:
    """This class implements filtering logic for Url objects.

    Attributes:
        accepted_exts: If specified, download only extensions in this list.
        rejected_exts: If specified, download only extensions NOT in this list.
        accepted_domains: If specified, follow only domains in this list.
        rejected_domains: If specified, follow only domains NOT in this list.
    """

    def __init__(self, accepted_exts=None, rejected_exts=None,
        accepted_domains=None, rejected_domains=None):
        """Iniziatlization of filter.

        Args:
            config: Configuration object.
        """

        self.accepted_exts = accepted_exts
        self.rejected_exts = rejected_exts
        self.accepted_domains = accepted_domains
        self.rejected_domains = rejected_domains

    def validate_domain(self, url):
        """Checks whether the given url object satisfies domain constraints."""

        accepted = (not self.accepted_domains) or \
            any([(domain in url.domain) for domain in self.accepted_domains])
        not_rejected = (not self.rejected_domains) or \
            all([(domain not in url.domain) for domain in self.rejected_domains])

        return accepted and not_rejected

    def validate_content(self, url):
        """Checks whether the given url object satisfies extension constraints."""

        accepted = (self.accepted_exts is None) or (url.ext in self.accepted_exts)
        not_rejected = (self.rejected_exts is None) or (url.ext not in self.rejected_exts)

        return accepted and not_rejected
