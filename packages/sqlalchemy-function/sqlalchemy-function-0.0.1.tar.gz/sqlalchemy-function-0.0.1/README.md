# SQLAlchemy-Function

SQLAlchemy-Function defines a [SQLALchemy Mixin](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html) for creating `Function` models.

A `Function` model has a parent (optional), a function, arguments, and keyword arguments. When called, the `Function` model executes its function, passing in its parent (if applicable), its arguments, and its keyword arguments.

## Example

Suppose we have a function, `foo`, which we want to store. We also want to store the arguments and keyword arguments with which we will later execute `foo`.

After setup, we can achieve this with the following:

```python
def foo(*args, **kwargs):
    print('My arguments are:', args)
    print('My keyword arguments are:', kwargs)
    return 'hello world'

f = Function(func=foo, args=['hello moon'], kwargs={'hello': 'star'})
session.add(f)
session.commit()
print(f())
```

Output:

```
My arguments are: ('hello moon',)
My keyword arguments are: {'hello': 'star'}
hello world
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/sqlalchemy-function](https://dsbowen.github.io/sqlalchemy-function).

## License

Publications which use this software should include the following citation for SQLAlchemy-Function and its dependency, [SQLAlchemy-Mutable](https://pypi.org/project/sqlalchemy-mutable/):

Bowen, D.S. (2019). SQLAlchemy-Function \[Computer software\]. [https://github.com/dsbowen/sqlalchemy-functionv](https://github.com/dsbowen/sqlalchemy-function)

Bowen, D.S. (2019). SQLAlchemy-Mutable \[Computer software\]. [https://github.com/dsbowen/sqlalchemy-mutable](https://github.com/dsbowen/sqlalchemy-mutable)

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-function/blob/master/LICENSE).