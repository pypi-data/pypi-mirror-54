ANTARES HTM Utilities
=========================

Welcome to the documentation for the ANTARES ``htm`` Python library.
This library's primary offering is its interface for working with Hierarchical 
Triangular Meshes (HTMs) as a means to index geospatial data. It offers this
functionality as a pure Python library and has no compilation dependencies on
particular database libraries.

Therefore this library is *not meant for use in performance-critical domains*.
If your indexing operations are tightly coupled to a relational database
I recommend using an application like `scisql`.

This library may be useful to you as part of a CI/CD setup or as an aid
in investigating non-relational database technology as a geospatial data
storage solution.

.. include:: contents.rst.inc
