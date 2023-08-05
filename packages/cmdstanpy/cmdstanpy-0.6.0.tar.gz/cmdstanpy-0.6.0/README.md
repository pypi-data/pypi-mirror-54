# CmdStanPy

CmdStanPy is a lightweight interface to Stan for Python users which
provides the necessary objects and functions to compile a Stan program
and run Stan's samplers.

### Goals

- Clean interface to Stan services so that CmdStanPy can keep up with Stan releases.

- Provides complete control - all sampler arguments have corresponding named argument
for CmdStanPy sampler function.

- Easy to install,
  + minimal Python library dependencies: numpy, pandas
  + Python code doesn't interface directly with c++, only calls compiled executables

- Modular - CmdStanPy produces a sample from the posterior, downstream modules do the analysis.

### Docs

See https://cmdstanpy.readthedocs.io/en/latest/index.html

### Source Repository

CmdStan's source-code repository is hosted here on GitHub.

### Licensing

The CmdStanPy, CmdStan, and the core Stan C++ code are licensed under new BSD.

### Example

::

    import os
    from cmdstanpy import CmdStanModel, cmdstan_path

    # specify Stan file, create, compile CmdStanModel object
    bernoulli_path = os.path.join(cmdstan_path(), 'examples', 'bernoulli', 'bernoulli.stan')
    bernoulli_model = CmdStanModel(stan_file=bernoulli_path)
    bernoulli_model.compile()


    # specify data, fit the model
    bernoulli_data = { "N" : 10, "y" : [0,1,0,0,0,0,0,0,0,1] }
    bernoulli_fit = bernoulli_model.sample(chains=5, cores=3, data=bernoulli_data)

    # summarize the results (wraps CmdStan `bin/stansummary`):
    bernoulli_fit.summary()
