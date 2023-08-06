# -*- coding: utf-8 -*-

class Pipe:
    """Class for pipeline component. It is subclassed by concrete components
    and it defines the interface that they should follow.
    """

    name = None

    def __init__(self, config):
        """Create a new pipe instance."""
        raise NotImplementedError

    def __call__(self, obj, **kwargs):
        """Apply the pipe to a single object, which is modified in-place and
        returned.
        __call__ should delegate to `set_annotations()` method.
        """
        self.set_annotations(obj, **kwargs)

        return obj

    def set_annotations(self, obj, **kwargs):
        """Implements the component processing on object."""
        raise NotImplementedError

    def to_disk(self, path, exclude=tuple(), **kwargs):
        """Serialize the pipe to disk."""
        pass

    def from_disk(self, path, exclude=tuple(), **kwargs):
        """Load the pipe from disk."""
        pass
