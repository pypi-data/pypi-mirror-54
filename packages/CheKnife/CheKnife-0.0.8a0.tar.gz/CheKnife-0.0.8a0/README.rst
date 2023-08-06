CheKnife
========

Python utilities compilation.

-  Free software: MIT license

Install
=======

::

   pip install CheKnife

Packages
========

| `CheKnife.pki <docs/CheKnife_pki.md>`__
| `CheKnife.django.choiceutils <docs/CheKnife.choiceutils.md>`__
| `CheKnife.hashing <docs/hashing.md>`__
| `CheKnife.logs <docs/CheKnife.logs.md>`__
| `CheKnife.files <docs/CheKnife.files.md>`__
| `CheKnife.security <docs/CheKnife.security>`__
| `CheKnife.ssl <docs/CheKnife.ssl.md>`__

Tests
=====

.. code:: bash

   nosetests --with-coverage --cover-inclusive --cover-package=CheKnife --cover-html

Upload to PyPi
==============

.. code:: bash

   python setup.py sdist upload -r pypi
