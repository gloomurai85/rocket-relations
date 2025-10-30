Welcome to rocket_relations's documentation!
============================================

This site documents the public API and includes a minimal example.

Quickstart
----------

.. code-block:: python

   from rocket_relations import c_star, c_f
   cs = c_star(gamma=1.2, R=350.0, T0=3500.0)           # ~1706.6214 m/s
   cf = c_f(gamma=1.2, pr_e=0.0125, pr_a=0.02, eps=10)  # ~1.5423079
   print(cs, cf)

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: API

   api
   tutorial

Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
