python-usda
===========

   ⚠️ Since October 1, 2019, the APIs this package relies on have been
   deprecated. python-usda 1.x will remove those APIs and rely on the new
   `Food Data Central`_ APIs.

python-usda is a fork of `pygov`_ focused on
`USDA's Food Composition Database API <usda>`_.
Have a look at the `documentation`_!

Setup
-----

::

  pip install python-usda

Usage
-----

.. code:: python

   from usda.client import UsdaClient

   client = UsdaClient("YOUR_API_KEY")
   foods = client.list_foods(5)

   for food in foods:
       print(food.name)

Result::

   Abiyuch, raw
   Acerola juice, raw
   Acerola, (west indian cherry), raw
   Acorn stew (Apache)
   Agave, cooked (Southwest)

.. _Food Data Central: https://fdc.nal.usda.gov/api-guide.html
.. _pygov: https://pypi.org/project/pygov/
.. _usda: http://ndb.nal.usda.gov/ndb/doc/
.. _documentation: https://lucidiot.gitlab.io/python-usda/
