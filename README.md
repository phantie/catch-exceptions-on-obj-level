# supreme-error-handler

Nothing's better than a good example:


```python
    class A:
        def foo(self): 1/0
        def bar(self): self.FourOFour
        def baz(self): int('eger')
        def itch(self): (lambda: 0)(42)

    @ruler
    class rules:
        @ruler(ZeroDivisionError, AttributeError)
        def handle(e):
            return f'Caught {e.__class__.__name__}!'

        @ruler(ValueError)
        def handle(e):
            return 'ValueError!'

        @ruler(Exception) # handle any other
        def handle(e):
            return f'Unexpected {e.__class__.__name__}!'

    a = A()
    protected = ProtectCalls(a, rules) # Does not modify the underlying object
                                       # It's just a proxy.

    assert protected.foo() == 'Caught ZeroDivisionError!'
    assert protected.bar() == 'Caught AttributeError!'
    assert protected.baz() == 'ValueError!'
    assert protected.itch() == 'Unexpected TypeError!'
    
    a.baz() # raises ValueError
```

Install

    pip install git+https://github.com/phantie/supreme-error-handler.git
    
Import

    from excepto import ProtectCalls, ruler
