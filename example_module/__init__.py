# Any names we define in __init__.py (or import into it!) will be accessible on the example module
# for example:
#     import example_module
#     example_module.x  -> 1
#     example_module.foo -> (not found!)
from example_module.__foo import x, y, z
from example_module.__bar import a, b, c

# Controls what you get if you `import * from example_module`
__all__ = [
    "x", "y", # omitting z
    "a", "b", # omitting c
]
