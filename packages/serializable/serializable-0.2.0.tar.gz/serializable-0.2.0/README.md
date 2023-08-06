[![Build Status](https://travis-ci.org/iskandr/serializable.svg?branch=master)](https://travis-ci.org/iskandr/serializable)

# serializable
Base class with serialization methods for user-defined Python objects

## Usage
Classes which inherit from `Serializable` are enabled with default implementations of
`to_json`, `from_json`, `__reduce__` (for pickling), and other serialization
helpers. 

A derived class must either:

* have a member data matching the name of each argument to `__init__`
* provide a user-defined `to_dict()` method which returns a dictionary whose keys match the arguments to `__init__`

If you change the keyword arguments to a class which derives from `Serializable` but would like to be able to deserialize older JSON representations then you can define a class-level dictionary called `_KEYWORD_ALIASES` which maps old keywords to new names (or `None` if a keyword was removed).

## Limitations

* Serializable objects must inherit from `Serializable`, be tuples or namedtuples, be serializble primitive types such as dict, list, int, float, or str.

* The serialized representation of objects relies on reserved keywords (such as `"__name__"`, and `"__class__"`), so dictionaries are expected to not contain any keys which begin with two underscores.
