===========================
fastapi-simple-cachecontrol
===========================

Cache-Control header management for FastAPI

Overview
========

Provide middleware to control Cache-Control header.

Installation
============

This package is not registered in PyPI. Wheel is stored in GitHub Releases.

.. code-block: sh

   # Using pip
   pip install https://github.com/attakei/fastapi-simple-cachecontrol/releases/download/v0.1.0/fastapi_simple_cachecontrol-0.1.0-py3-none-any.whl
   # Using poetry
   poetry add https://github.com/attakei/fastapi-simple-cachecontrol/releases/download/v0.1.0/fastapi_simple_cachecontrol-0.1.0-py3-none-any.whl

Usage
=====

Adding header for all request
-----------------------------

.. code-block:: python

   from fastapi import FastAPI
   from fastapi_simple_cachecontrol.types import CacheControl
   from fastapi_simple_cachecontrol.middleware import CacheControlMiddleware

   app = FastAPI()
   app.add_middleware(CacheControlMiddleware, cache_control=CacheControl("public"))

Specs
=====

* You can select only one of cacheability directives.

  * Supporting ``public``, ``private``, ``no-cache`` and ``no-store``

* Expires directives are used as value if only used ``public`` or ``private``.

Refs
====

* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
