HTM Operations
==============

Finding the HTM ID of a Coordinate
----------------------------------

.. code:: python

   >>> from htm import get_htm_id
   >>> ra = 100 # degrees
   >>> dec = -15 # degrees
   >>> get_htm_id(ra, dec, level=20)
   10148770484434
   

Computing HTM IDs for a Cone Search
-----------------------------------

.. code:: python

   >>> import htm
   >>> from htm import get_htm_circle_region
   >>> ra = 100 # degrees
   >>> dec = -15 # degrees
   >>> radius = htm.constants.ARCSEC_PER_DEGREE / 4 # degrees
   >>> get_htm_circle_region(ra, dec, radius, level=20)
   [(10148770484369, 10148770484369),
    (10148770484374, 10148770484374),
    (10148770484382, 10148770484382),
    (10148770484433, 10148770484435),
    (10148770484441, 10148770484441),
    (10148770484445, 10148770484447)]

This function takes the following required parameters:

* ``ra`` (float, degrees)
* ``dec`` (float, degrees)
* ``radius`` (float, degrees)
* ``level`` (int)

You can also supply an argument to ``max_ranges`` which will adaptively
coarsen the level of the returned HTM ranges to constrain the length
of the list.

.. code:: python

   >>> from htm import get_htm_circle_region
   >>> ra = 100 # degrees
   >>> dec = -15 # degrees
   >>> radius = htm.constants.ARCSEC_PER_DEGREE / 4 # degrees
   >>> get_htm_circle_region(ra, dec, radius, level=20, max_ranges=3)
   [(10148770484368, 10148770484383),
    (10148770484432, 10148770484447)]

By default ``get_htm_circle_region`` sets ``max_ranges`` to 256.
