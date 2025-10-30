# rocket_relations

Short description: Basic ideal rocket relations (`c*` and `CF`) for quick studies.

------------------------

## What this package does

Implements two ideal rocket performance relations:

- **Characteristic velocity**  
  \( c^* = \sqrt{\frac{1}{\gamma}\left(\frac{\gamma+1}{2}\right)^{\frac{\gamma+1}{\gamma-1}} R T_0} \)

- **Thrust coefficient (ratios form)**  
  \( CF = \sqrt{\frac{2\gamma^2}{\gamma-1}\left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{\gamma-1}}\!\left(1-(pr_e)^{\frac{\gamma-1}{\gamma}}\right)} + (pr_e - pr_a)\,\epsilon \)

Where:
- \(\gamma\): ratio of specific heats (> 1)  
- \(R\): specific gas constant (> 0)  
- \(T_0\): chamber (stagnation) temperature (> 0 K)  
- \(pr_e = p_e/p_0 \in [0,1)\), \(pr_a = p_a/p_0 \in [0,1)\)  
- \(\epsilon = A_e/A^* \ge 1\)

**Assumptions:** calorically perfect gas, steady, quasi-1D, isentropic nozzle flow, choked at the throat; neglect viscous/thermal/body forces.

------------------------

## Installation

Download the source code or clone the repo locally.
In the project root directory, open a terminal and create/activate
a fresh environment (or reuse an existing one) and install in editable mode:

```
bash
# create/activate any Python >=3.10 environment
conda create -n rocketenv python=3.12 -y
conda activate rocketenv

# from repo root
pip install -e .

#verify import
python -c "import rocket_relations as rr; print(rr.__all__)"
```
------------------------

## Quickstart

```
bash
from rocket_relations import c_star, c_f

cs = c_star(gamma=1.2, R=350.0, T0=3500.0)           # ~1706.6214 m/s
cf = c_f(gamma=1.2, pr_e=0.0125, pr_a=0.02, eps=10)  # ~1.5423079

print(cs, cf)

# Where to find the details
import rocket_relations as rr
help(rr)
help(rr.c_star)
help(rr.c_f)
```

------------------------

## Test

This repo uses pytest.

```
bash
pip install pytest
pytest -q
```

You should see all tests passing

------------------------

## Package Layout

```
bash
rocket-relations/           # repo root
├── pyproject.toml
├── README.md
├── src/
│   └── rocket_relations/
│       ├── __init__.py     # package docstring + re-export API
│       └── ideal.py        # c_star(...) and c_f(...)
└── tests/
    └── test_ideal.py       # unit tests
```







