=============================
django-pwny
=============================

.. image:: https://travis-ci.com/PsypherPunk/django-pwny.png?branch=master
   :target: https://travis-ci.com/PsypherPunk/django-pwny

*Have I Been Pwned?* password validator. Inspired by a
`blog post <https://www.thedatashed.co.uk/2019/02/07/django-pwny/>`_ on the subject.

Quickstart
----------

Install django-pwny::

    pip install django-pwny

Add it to your `AUTH_PASSWORD_VALIDATORS`:

.. code-block:: python

    AUTH_PASSWORD_VALIDATORS = [
        ...
        "pwny.validation.HaveIBeenPwnedValidator",
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
    (myenv) $ pip install Django requirements/test.txt
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

