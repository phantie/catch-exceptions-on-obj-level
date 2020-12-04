# catch-exceptions-on-obj-level

Nothing's better than a good example:


```python
    class A:
        def foo(self):
            return 1/0

        def bar(self):
            return self.FourOFour

        def baz(self):
            return int('eger')

        def itch(self):
            return (lambda: 0)(1, 2, 3)

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

    protected = ProtectCalls(A(), rules)

    assert protected.foo() == 'Caught ZeroDivisionError!'
    assert protected.bar() == 'Caught AttributeError!'
    assert protected.baz() == 'ValueError!'
    assert protected.itch() == 'Unexpected TypeError!'
```