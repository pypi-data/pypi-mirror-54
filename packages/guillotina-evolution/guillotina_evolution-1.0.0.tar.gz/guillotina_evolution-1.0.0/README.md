# guillotina_evolution


[![Build Status](https://travis-ci.org/vinissimus/guillotina_evolution.svg?branch=master)](https://travis-ci.org/vinissimus/guillotina_evolution) [![PyPI version](https://badge.fury.io/py/guillotina-evolution.svg)](https://badge.fury.io/py/guillotina-evolution) [![Codcov](https://codecov.io/gh/vinissimus/guillotina_evolution/branch/master/graph/badge.svg)](https://codecov.io/gh/vinissimus/guillotina_evolution/branch/master) ![](https://img.shields.io/pypi/pyversions/guillotina_evolution.svg)

Addon that provides evolutions/migrations to create or update objects in your Guillotina containers.


## Install

```console
pip install guillotina_evolution
```


## Configure

Add the following values in `app_settings`:

```python
app_settings = {
    "applications": [
        "guillotina_evolution",
    ],
    "commands": {
        "g-evolve": "guillotina_evolution.commands.evolve.EvolveCommand",
    },
```

Configure your app addon to initialize guillotina_evolution when is installed:

```python
from guillotina.component import get_utility
from guillotina_evolution.interfaces import IEvolutionUtility

@configure.addon(name="app", title="Your guillotina app")
class ManageAddon(Addon):
    @classmethod
    async def install(cls, container, request):
        utility = get_utility(IEvolutionUtility)
        utility.install()  # initialize current generation with the greatest registered generation

        # ...
```


## Write your evolver

Create a folder `evolutions` inside your guillotina app that contains the following files:

`app/evolutions/__init__.py`
```python
from .r20190118 import *  # noqa
# Don't forget to add all rXXXXXXXX.py!
```

`app/evolutions/r20190118.py`
```python
from guillotina_evolution.utils import register_evolution

@register_evolution(1)
async def evolver(container):
    async for item in container.async_items():
        item.title = item.title + ' (Migrated)'
        item.register()
```

Update the `includeme()` of your app:

`app/__init__.py`
```python
def includeme(root):
    # ...
    configure.scan("app.evolutions")
```


## Evolve

Run guillotina command `g-evolve` to run your migrations.

```console
g -c config.yaml g-evolve
```
