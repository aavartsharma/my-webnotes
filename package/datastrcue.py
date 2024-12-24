class EnumMeta(type):
    """Metaclass to create Enum classes."""
    def __new__(cls, name, bases, dct):
        members = {k: v for k, v in dct.items() if not k.startswith('_')}
        enum_class = super().__new__(cls, name, bases, dct)
        enum_class._members_ = members
        for key, value in members.items():
            setattr(enum_class, key, enum_class(key, value))
        return enum_class

    def __getitem__(cls, item):
        """Access member by name."""
        return cls._members_[item]
    
    def __iter__(cls):
        """Iterate over members."""
        return iter(cls._members_.values())

    def __contains__(cls, item):
        """Check if name exists in enum."""
        return item in cls._members_


class Enum(metaclass=EnumMeta):
    """Base Enum class."""
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name}: {self._value}>"

    def __str__(self):
        return f"{self._name}"

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self._name == other._name and self._value == other._value
        return NotImplemented

    def __hash__(self):
        return hash((self._name, self._value))


