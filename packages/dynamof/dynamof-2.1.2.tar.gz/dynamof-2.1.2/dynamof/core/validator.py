
validators = {}

def validator(func):
    validators[func.__name__] = func
    return func

def validate(**kwargs):
    for key, value in kwargs.items():
        validating_func = validators[key]
        if validating_func is None:
            raise TypeError(f'A validator could not be found for - {key}. Do you need to implement one?')
        validating_func(value)

def enforce_attrs(obj, required, optional=None, strict=True):
    """Returns true if the given object contains all the attributes
    specified in the given attrs list of attribute names. else false"""

    obj = obj or {}
    optional = optional or {}

    required_keys = required.keys()
    all_keys = required_keys + optional.keys()

    keys = obj.keys()

    contains_required = lambda: set(required_keys).issubset(keys)
    only_contains_allowed = lambda: strict is False or set(keys).issubset(all_keys)

    return contains_required() and only_contains_allowed()

@validator
def lsi(obj):
    """Validates that the given objects meets the model
    requirements to be a local secondary index argument
    to an operation"""
    return enforce_attrs(obj,
        required={
            'name': str,
            'keys': [str, dict]
        })

@validator
def gsi(obj):
    """Validates that the given objects meets the model
    requirements to be a global secondary index argument
    to an operation"""
    return enforce_attrs(obj,
        required=[
            'name',
            'keys'
        ],
        optional=[
            'throughput'
        ])
