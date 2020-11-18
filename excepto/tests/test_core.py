from excepto import *
import pytest

@pytest.fixture
def basic_inst():
    class A:
        handle = to_what = rules = 0

        def foo(self): return 1/0
        def bar(self): return 1/0
        def baz(self): return self.k

    a = A()
    return a

def test_proxied_no_collisions(basic_inst):

    proxied_inst = ProtectCalls(basic_inst, rules = {})
    assert all(getattr(proxied_inst, name) == 0 for name in ("handle","to_what","rules"))

def test_works_according_to_rules(basic_inst):
    proxied_inst = ProtectCalls(basic_inst, 
    rules = {
        ZeroDivisionError: lambda e: 'Impossible!',
        AttributeError: lambda e: 'No attribute! Whatever, at least no exceptions.'})

    assert proxied_inst.foo() == 'Impossible!'
    assert proxied_inst.bar() == 'Impossible!'
    assert proxied_inst.baz() == 'No attribute! Whatever, at least no exceptions.'

def test_ruler():
    @ruler
    class rules:
        @ruler(ZeroDivisionError)
        def handle(e):
            return 'Impossible!'

        @ruler(AttributeError)
        def handle(e):
            return 'No attribute! Whatever, at least no exceptions.'

    @ruler
    class rare_rules:
        @ruler(OverflowError)
        def handle(e):
            return 'wtf is this C'

        @ruler(MemoryError)
        def handle(e):
            return 'unlucko'

    sets_of_rules = (rules, rare_rules) # Dict[Type[Exception], Callable[[Exception], Any]] each

    assert all(isinstance(o, dict) for o in sets_of_rules)

    assert all(k in rules for k in (ZeroDivisionError, AttributeError))
    assert all(k in rare_rules for k in (OverflowError, MemoryError))
    assert all(v.__name__ == 'handle' for set_of_rules in sets_of_rules
                                        for v in set_of_rules.values())

def test_does_not_catch_AttibuteError_if_not_inside_a_function(basic_inst):
    @ruler
    class rules:
        @ruler(AttributeError)
        def handle(e):
            return 'No attribute! Whatever, at least no exceptions.'

    proxied_inst = ProtectCalls(basic_inst, rules)

    assert proxied_inst.baz() == 'No attribute! Whatever, at least no exceptions.'
    with pytest.raises(AttributeError):
        proxied_inst.k