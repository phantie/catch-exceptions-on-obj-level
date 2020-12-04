class ProtectCalls:
    def __init__(self, to_what, rules):
        def generalize_rules(rules):
            def process_exception(e):
                for eType in type(e).__mro__[:-1]:
                    try:
                        return rules[eType](e)
                    except KeyError:
                        pass
                raise e
            return process_exception

        self.to_what = to_what
        self.exps = tuple(rules.keys())
        assert all(issubclass(eType, BaseException) for eType in rules.keys()), \
            f'Every key in rules must subclass {BaseException}'

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

class ruler:
    rules = {}

    def __call__(self, *exceptions):
        assert all(isinstance(e, type) for e in exceptions)
        if len(exceptions) == 1 and not issubclass(exceptions[0], BaseException):
            _ = self.rules.copy()
            self.rules.clear()
            return _
        else:
            return lambda h: tuple(self.rules.__setitem__(e, h) for e in exceptions)

ruler = ruler()