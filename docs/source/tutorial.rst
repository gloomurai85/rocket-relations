Tutorial
========

.. note::

   **Assumptions**: calorically perfect gas; steady, quasi-1D, isentropic nozzle flow;
   choked at the throat; neglect viscous/thermal/body forces.


This short walkthrough shows how to compute the two relations and interpret inputs.

Setup
-----

.. code-block:: bash

   # from repo root
   pip install -e .
   python -c "import rocket_relations as rr; print(rr.__all__)"

Compute ``c*`` and ``CF``
-------------------------

.. code-block:: python

   from rocket_relations import c_star, c_f

   # Characteristic velocity (SI units)
   cs = c_star(gamma=1.2, R=350.0, T0=3500.0)
   print("c* [m/s]:", cs)

   # Thrust coefficient using pressure/area ratios
   cf = c_f(gamma=1.2, pr_e=0.0125, pr_a=0.02, eps=10.0)
   print("CF [-]:", cf)

Notes on inputs
---------------

- ``gamma`` must be > 1 (calorically perfect gas model).
- ``R`` and ``T0`` must be positive; ``T0`` is in Kelvin.
- ``pr_e = p_e/p_0`` and ``pr_a = p_a/p_0`` must be in ``[0, 1)``.
- ``eps = A_e/A*`` must be ``>= 1``.

Validation
----------

These functions raise ``TypeError`` for non-numerics and ``ValueError`` for out-of-range inputs.

See also
--------

- :mod:`rocket_relations`
- :mod:`rocket_relations.ideal`