# -*- coding: utf-8 -*-

class Pipeline:
    """Base class for generic processing pipeline.

    Implementes methods for creating and organizing processing components,
    aka pipes.

    Attributes:
        factories: A dict with build functions for creating components.
        _pipeline: A list of registered components.
    """

    def __init__(self, factories):

        self.factories = factories
        self._pipeline = []

    @property
    def pipe_names(self):
        """Get names of registered components in pipeline. """

        return [name for name, _ in self._pipeline]

    def create_pipe(self, name, config):
        """Create a pipeline component from a factory.

        Component must be present in factories.
        """

        if name not in self.factories:
            raise KeyError('Component not supported')

        factory = self.factories[name]

        return factory(config)

    def add_pipe(self, component, name=None, pos=None, before=None,
        after=None):
        """Add a component to the processing pipeline.

        Valid components are callables and take a `News` object, modify it and
        return it.

        Only one of pos and before/after can be set.

        Args:
            component: A valid component which subclasses BaseComponent.
            name: Name of the component, if specified overrides the default one.
            pos: Position in pipeline. Valid options are: "last" (default),
                "first".
            before: Component name to insert component directly before.
            after: Component name to insert component directly after.
        """

        if not hasattr(component, '__call__'):
            msg = f'Component {component} must be callable'
            raise ValueError(msg)

        if sum([bool(pos), bool(before), bool(after)]) > 1:
            raise ValueError('Only one of "pos" and "before"/"after" can be set.')

        # get component name
        if name is None:
            if hasattr(component, 'name'):
                name = component.name
            else:
                name = repr(component)

        # no duplicates
        if name in self.pipe_names:
            raise ValueError('Component already registered')

        pipe = (name, component)

        if pos == 'last' or not any([pos, before, after]):
            self._pipeline.append(pipe)
        elif pos == 'first':
            self._pipeline.insert(0, pipe)
        elif before and before in self.pipe_names:
            self._pipeline.insert(self.pipe_names.index(before), pipe)
        elif after and after in self.pipe_names:
            self._pipeline.insert(self.pipe_names.index(after) + 1, pipe)
        else:
            raise ValueError('Position not supported')

    def has_pipe(self, name):
        """Check if a component name is present in the pipeline.

        Equivalent to `name in pipeline.pipe_names`.
        """
        return name in self.pipe_names
