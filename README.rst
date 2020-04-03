===========================
fastapi-simple-cachecontrol
===========================

Cache-Control header management for FastAPI

Overview
========

Provide middleware to control Cache-Control header.

Installation
============

(now writing)

Usage
=====

Adding header for all request
-----------------------------

.. code-block:: python

   from fastapi import FastAPI
   from fastapi_simple_cachecontrol import CacheControl
   from fastapi_simple_cachecontrol.middleware import CacheControlMiddleware

   app = FastAPI()
   app.add_middleware(CacheControlMiddleware, header=CacheControl("public"))


Refs
====

* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
