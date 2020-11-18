__all__ = ['ProtectCalls', 'ruler']

class ProtectCalls:
    def __init__(self, to_what, rules):
        def generalize_rules(rules):
            return lambda e: rules[type(e)](e)

        self.to_what = to_what
        self.exps = tuple(rules.keys())
        self.handle = generalize_rules(rules)

    def __getattribute__(self, name):
        def self_getattr(name):
            return object.__getattribute__(self, name)

        attr = object.__getattribute__(self_getattr('to_what'), name)
        if callable(attr):
            def wrap(*args, **kwargs):
                try:
                    return attr(*args, **kwargs)
                except self_getattr('exps') as e:
                    return self_getattr('handle')(e)
            return wrap

        else:
            return attr

def init(cls): 
    return cls()

@init
class ruler:
    rules = {}

    def __call__(self, o):
        assert isinstance(o, type)
        if issubclass(o, Exception):
            return lambda h: self.rules.__setitem__(o, h) 
        else:
            result = self.rules.copy()
            self.rules.clear()
            return result