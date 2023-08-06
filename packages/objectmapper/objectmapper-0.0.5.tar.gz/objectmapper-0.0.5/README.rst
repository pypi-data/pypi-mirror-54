objectmapper
============

A small module for mapping between object types.

* `Documentation <https://objectmapper.readthedocs.io/en/latest/>`_
* `Source <https://github.com/ABoiledCarny/objectmapper>`_
* `PyPi Package <https://pypi.org/project/objectmapper/>`_

Installation
------------
``objectmapper`` requires ``Python >= 3.6`` because it relies on modern type annotations.
::

   pip install objectmapper

Example
-------

>>> import objectmapper
>>> mapper = objectmapper.ObjectMapper()
>>> def int_to_str(i: int) -> str:
...     return str(i)
>>> mapper.create_map(int, str, int_to_str)
>>> mapper.map(42, str)
'42'
