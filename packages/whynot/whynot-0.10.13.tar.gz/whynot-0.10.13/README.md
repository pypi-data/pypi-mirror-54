# WhyNot [![Build Status](https://travis-ci.com/millerjohnp/whynot.svg?token=ERpRX6SmHRsKJ8dNb4QV&branch=master)](https://travis-ci.com/millerjohnp/whynot)
Statistical validity of causal inference methods using simulation.

Check out the [documentation!](https://people.eecs.berkeley.edu/~miller_john/whynot/)


## Basic installation instructions
1. (Optionally) create a virtual environment
```
python3 -m venv whynot-env
source whynot-env/bin/activate
```
2. Install via pip
```
pip install whynot
```

## Using other estimators
WhyNot is shipped with a small set of causal estimators written in pure Python.
To access other estimators, please install the companion library `whynot_estimators`
(https://github.com/millerjohnp/whynot_estimators), which includes a host of
state-of-the-art causal inference methods implemented in R.

To get the basic framework, run
```
pip install whynot_estimators
```
If you have R installed, you can install the `causal_forest` estimator by using
```
python -m  whynot_estimators install causal_forest
```
See `whynot_estimators` (https://github.com/millerjohnp/whynot_estimators) for
instructions on installing specific estimators, especially if you do not have an
existing R build.
