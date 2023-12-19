import inspect

from datetime import datetime


TYPE_KEY = "__type"


def _write(self, value):
    dict = {
        TYPE_KEY: value.__class__.__name__, 
    }
    for k, v in value.__dict__.items():
        if callable(v) or v is None:
            continue
        dict[k] = JsonFormat.get_format(v).write(v)
    return dict


def read_func(target_cls):
    def _read(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"{value} cannot be parsed by {target_cls.__name__}")

        _type = value.get(TYPE_KEY)
        if _type not in self._type_names:
            raise ValueError(f"{value} cannot be read as {self._types}")
        
        target_instance = target_cls.__new__(target_cls)
        for k, v in value.items():
            if k == TYPE_KEY:
                continue
            setattr(target_instance, k, JsonFormat.get_format(v).read(v))
        
        return target_instance
    return _read


class JsonMixinMeta(type):
    def __new__(metacls, name, bases, dct):
        # Create the subclass normally
        cls = super().__new__(metacls, name, bases, dct)

        # Check if this is a subclass (not the base class itself)
        if bases:
            # Define json format class
            formatter_name = f"{name}JsonFormat"
            json_format_class = type(
                formatter_name,
                (JsonFormat,),
                {
                    "_types": [cls],
                    "write": _write,
                    "read": read_func(cls),
                }
            )
            cls.json_format = json_format_class()

            # set attribute default value to None
            if '__init__' in dct:
                args = inspect.getfullargspec(dct['__init__']).args[1:]
                for arg in args:
                    if arg not in dct:
                        setattr(cls, arg, None)

        return cls


class JsonMixin(metaclass=JsonMixinMeta):
    def to_json(self):
        return self.json_format.write(self)

    @classmethod
    def from_json(cls, value):
        return cls.json_format.read(value)


class JsonFormatMeta(type):
    _registry = {}

    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        if bases:
            types = dct.get("_types")
            if types is None or len(types) == 0:
                raise TypeError(f"_typs is missing in {name} definition")
            for _type in types:
                JsonFormat._registry[_type.__name__] = cls
        return cls


class JsonFormat(metaclass=JsonFormatMeta):
    _types = None

    @classmethod
    def get_format(cls, value):
        registered_format = None
        if isinstance(value, dict):
            registered_format = JsonFormatMeta._registry.get(value.get(TYPE_KEY)) or (
                JsonFormatMeta._registry.get(value.__class__.__name__))
        else:
            registered_format = JsonFormatMeta._registry.get(value.__class__.__name__)

        if registered_format is None:
            raise ValueError(f"{value.__class__}: {value} isn't supported by json formatting")

        return registered_format()
    
    @property
    def _type_names(self):
        return [_type.__name__ for _type in self._types]    

    def write(self, value):
        raise NotImplementedError
    
    def read(self, value):
        raise NotImplementedError
    

class NativeJsonFormat(JsonFormat):
    _types = (str, int, float, bool)

    def write(self, value):
        return value

    def read(self, value):
        return value
    

class ListJsonFormat(JsonFormat):
    _types = [list, tuple]
    def write(self, value):
        return [
            JsonFormat.get_format(item).write(item)
            for item in value
        ]
    
    def read(self, value):
        return [
            JsonFormat.get_format(item).read(item)
            for item in value
        ]
    

class DateTimeFormat(JsonFormat):
    _types = [datetime]

    def write(self, value):
        return {
            TYPE_KEY: datetime.__name__,
            "value": value.isoformat(),
        }
    
    def read(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"{value.__class__}: {value} cannot be parsed by datetime json format")

        if value.get(TYPE_KEY) != datetime.__name__:
            raise ValueError("%s cannot be parsed by DateTimeFormat")
        return datetime.fromisoformat(value["value"])


class DictJsonFormat(JsonFormat):
    _types = [dict]
    def write(self, value):
        target = {
            JsonFormat.get_format(k).write(k): JsonFormat.get_format(v).write(v)
            for k, v in value.items()
        }
        target[TYPE_KEY] = dict.__name__
        return target

    
    def read(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"{value} cannot be parsed by dict json format")

        _type = value.get(TYPE_KEY)
        if _type not in self._type_names:
            raise ValueError(f"{value} cannot be read as {self._types}")

        return {
            JsonFormat.get_format(k).read(k): JsonFormat.get_format(v).read(v)
            for k, v in value.items() if k != TYPE_KEY
        }
