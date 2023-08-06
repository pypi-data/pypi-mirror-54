# -*- coding: utf-8 -*-
from .pipeline import Pipeline

class Processor(Pipeline):
    """Abstract class for pipeline processing.

    Creates and executes the processing pipeline on data object.
    """

    def __init__(self, config, factories):
        """Processor inizialization."""

        # init pipeline
        super().__init__(factories)
        self.config = config

    def __call__(self, input, disable=[], pipe_cfg=None):
        """Apply the pipeline to given input.

        The text can span multiple sentences, and can contain arbtrary
        Args:
            input: The input to be processed.
            disable (list): Names of the pipeline components to disable.
            pipe_cfg (dict): An optional dictionary with extra keyword arguments
                for specific components.

        Returns:
            obj (Object): A generic container for accessing the annotations.

        """

        obj = self.make_obj(input)

        if pipe_cfg is None:
            pipe_cfg = {}

        for name, pipe in self._pipeline:
            if name in disable:
                continue
            if not hasattr(pipe, "__call__"):
                raise ValueError('Component must be callable.')

            obj = pipe(obj, **pipe_cfg.get(name, {}))

            if obj is None:
                raise ValueError(f'Pipeline component "{name}" returned None.')

        return obj

    def make_obj(self, input):
        """Creates the data object passing through the pipeline.
        This method must be implemented by the concrete class."""
        raise notImplementedError('Concrete processors must override this method.')
