=============================
dj-input-googlesheets
=============================

.. image:: https://badge.fury.io/py/dj-input-googlesheets.svg
    :target: https://badge.fury.io/py/dj-input-googlesheets

.. image:: https://travis-ci.org/kverdecia/dj-input-googlesheets.svg?branch=master
    :target: https://travis-ci.org/kverdecia/dj-input-googlesheets

.. image:: https://codecov.io/gh/kverdecia/dj-input-googlesheets/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kverdecia/dj-input-googlesheets

Input rows from google sheets into input-flow

Documentation
-------------

The full documentation is at https://dj-input-googlesheets.readthedocs.io.

Quickstart
----------

Install dj-input-googlesheets::

    pip install dj-input-googlesheets

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'inputgooglesheets.apps.InputGoogleSheetsConfig',
        ...
    )

Add dj-input-googlesheets's URL patterns:

.. code-block:: python

    from inputgooglesheets import urls as inputgooglesheets_urls


    urlpatterns = [
        ...
        url(r'^', include(inputgooglesheets_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
