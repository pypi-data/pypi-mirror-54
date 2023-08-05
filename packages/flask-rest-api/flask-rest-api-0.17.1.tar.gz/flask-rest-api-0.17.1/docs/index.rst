flask-rest-api: build a REST API on Flask using Marshmallow
===========================================================

Release v\ |version|. (:ref:`Changelog <changelog>`)

**Deprecation warning**: flask-rest-api has been renamed to flask-smorest_.

------------------------------------------------------------

**flask-rest-api** is a framework library for creating REST APIs.

It uses Flask as a webserver, and marshmallow_ to serialize and deserialize data.
It relies extensively on the marshmallow ecosystem, using webargs_ to get arguments
from requests, and apispec_ to generate an OpenAPI_ specification file as
automatically as possible.


Install
=======

flask-rest-api requires Python >= 3.5.

.. code-block:: bash

    $ pip install flask-rest-api


Guide
=====

.. toctree::
    :maxdepth: 1

    quickstart
    arguments 
    response
    pagination
    etag
    openapi


API Reference
=============

.. toctree::
    :maxdepth: 2

    api_reference

Project Info
============

.. toctree::
    :maxdepth: 1

    changelog
    license
    authors



.. _marshmallow: https://marshmallow.readthedocs.io/
.. _webargs: https://webargs.readthedocs.io/
.. _apispec: https://apispec.readthedocs.io/
.. _flask-smorest: https://flask-smorest.readthedocs.io/
.. _OpenAPI: https://www.openapis.org/
