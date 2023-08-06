# Conan Utility For Visual Studio Code

## Overview
This package provides a helper method for a [Conan](https://conan.io) project's conanfile.py to update the Visual Studio Code C++ Tools plugin after installing dependencies, so that Intellisense finds the installed paths

## How to use
Use a [conanfile.py](https://docs.conan.io/en/latest/reference/conanfile.html) instead of conanfile.txt to define your project dependencies.

Then, in your class, add an event handler for ```imports```:
```python
#...
from parktoma.vscconan import update_cpp_tools

class MyProject(ConanFile):
    #...
    def imports(self):
        update_cpp_tools(self, conanfile_path=__file__)
```

