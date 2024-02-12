# Python Discussion Series

Some example code that explains various Python features and concepts.

Requirements: This code depends mostly on core Python 3, but does also cover PyTest and relies on its test discovery features. (By default, GitPod uses Python 3.12.1.)

Gitpod should install the requirements automatically, but the manual equivalent would be:
```
pip install -r requirements.txt
```

## main.py
A typical "entry point" for a script, including some usage of StringIO for simulating file-like objects

## test_example.py
Several pytest tests and fixtures

## example_module
An example module, including an [__init__.py](example_module/__init__.py), some "private" files ([_foo.py](example_module/__foo.py) and [__bar.py](example_module/__bar.py)), a nested [conftest.py](example_module/tests/conftest.py), and some examples of how tests and fixture discovery work in subfolders
