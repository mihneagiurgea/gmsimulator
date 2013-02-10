class BaseUnit(object):
    """Abstract base class for a unit.

    Performs attribute storage and a few handy properties.
    """

    # List mapping internal attributes names to their actual names.
    # Must be set by subclasses.
    ATTRIBUTES = None

    # All units have a base speed of 5 for now.
    speed = 5

    def __init__(self, name, **kwargs):
        self.name = name

        for attribute, name in self.ATTRIBUTES:
            setattr(self, attribute, kwargs.pop(attribute, 0))

        if kwargs:
            raise ValueError('Invalid attributes: %s' % kwargs)

        self.strategy = None

    def __repr__(self):
        pieces = []
        for attribute, name in self.ATTRIBUTES:
            value = getattr(self, attribute)
            if value:
                pieces.append('%s %s' % (value, name))
        return '%s: %s' % (self.name, ' '.join(pieces))

    def __str__(self):
        return self.name

    @property
    def move_distance(self):
        return self.speed

    @property
    def run_distance(self):
        return 2 * self.speed

    def act(self, game_state):
        """Use the associated strategy class to act."""
        if self.strategy is None:
            raise AttributeError('Cannot act - missing strategy.')
        self.strategy.act(self, game_state)