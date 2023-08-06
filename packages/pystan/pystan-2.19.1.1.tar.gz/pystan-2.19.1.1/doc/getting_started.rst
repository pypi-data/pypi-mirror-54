.. _getting-started:

.. currentmodule:: pystan

=================
 Getting started
=================

PyStan is the `Python <http://python.org>`_ interface for
`Stan <http://mc-stan.org/>`_.

Prerequisites
=============

PyStan has the following dependencies:

- `Python <http://python.org>`_: 2.7, >=3.3
- `Cython <http://cython.org>`_: >=0.22
- `NumPy <http://numpy.org>`_: >=1.7

PyStan also requires that a C++ compiler be available to Python during
installation and at runtime. On Debian-based systems this is accomplished by
issuing the command ``apt-get install build-essential``.

Installation
============

.. note:: Installing PyStan involves compiling Stan. This may take
    a considerable amount of time.

Unix-based systems including Mac OS X
-------------------------------------

PyStan and the required packages may be installed from the `Python Package Index
<https://pypi.python.org/pypi>`_ using ``pip``.

::

   pip install pystan

Mac OS X users encountering installation problems may wish to consult the
`PyStan Wiki <https://github.com/stan-dev/pystan/wiki>`_ for possible solutions.

Windows
-------

PyStan on Windows requires Python 2.7/3.x and a working C++ compiler.  If
you have already installed Python and the MingW-w64 C++ compiler,
running ``pip install pystan`` will install PyStan.

If you need to install a C++ compiler, you will find detailed installation
instructions in :ref:`windows`.

Using PyStan
============

The module's name is ``pystan`` so we load the module as follows:

.. code-block:: python

    import pystan

Example 1: Eight Schools
------------------------

The "eight schools" example appears in Section 5.5 of Gelman et al. (2003),
which studied coaching effects from eight schools.

.. code-block:: python

    schools_code = """
    data {
        int<lower=0> J; // number of schools
        vector[J] y; // estimated treatment effects
        vector<lower=0>[J] sigma; // s.e. of effect estimates
    }
    parameters {
        real mu;
        real<lower=0> tau;
        vector[J] eta;
    }
    transformed parameters {
        vector[J] theta;
        theta = mu + tau * eta;
    }
    model {
        eta ~ normal(0, 1);
        y ~ normal(theta, sigma);
    }
    """

    schools_dat = {'J': 8,
                   'y': [28,  8, -3,  7, -1,  1, 18, 12],
                   'sigma': [15, 10, 16, 11,  9, 11, 10, 18]}

    sm = pystan.StanModel(model_code=schools_code)
    fit = sm.sampling(data=schools_dat, iter=1000, chains=4)

In this model, we let ``theta`` be transformed parameters of ``mu`` and ``eta``
instead of directly declaring theta as parameters. By parameterizing this way,
the sampler will run more efficiently.

In PyStan, we can also specify the Stan model using a file. For example, we can
download the file :download:`8schools.stan <8schools.stan>` into
our working directory and use the following call to ``stan`` instead:

.. code-block:: python

    sm = pystan.StanModel(file='8schools.stan')
    fit = sm.sampling(data=schools_dat, iter=1000, chains=4)

Once a model is compiled, we can use the StanModel object multiple times.
This saves us time compiling the C++ code for the model. For example, if we
want to sample more iterations, we proceed as follows:

.. code-block:: python

    fit2 = sm.sampling(data=schools_dat, iter=10000, chains=4)

The object ``fit``, returned from function ``stan`` stores samples from the
posterior distribution. The ``fit`` object has a number of methods, including
``plot`` and ``extract``. We can also print the ``fit`` object and receive
a summary of the posterior samples as well as the log-posterior (which has the
name ``lp__``).

The method ``extract`` extracts samples into a dictionary of arrays for
parameters of interest, or just an array.

.. code-block:: python

    la = fit.extract(permuted=True)  # return a dictionary of arrays
    mu = la['mu']

    ## return an array of three dimensions: iterations, chains, parameters
    a = fit.extract(permuted=False)

.. code-block:: python

    print(fit)

If `matplotlib <http://matplotlib.org/>`_ and
`scipy <http://http://www.scipy.org/>`_ are installed, a visual summary may
also be displayed using the ``plot()`` method.

.. code-block:: python

    fit.plot()
