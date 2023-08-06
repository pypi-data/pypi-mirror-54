# Guillotina link integrity

[![Travis CI](https://travis-ci.org/guillotinaweb/guillotina_linkintegrity.svg?branch=master)](https://travis-ci.org/guillotinaweb/guillotina_linkintegrity)
[![Test Coverage](https://codecov.io/gh/guillotinaweb/guillotina_linkintegrity/branch/master/graph/badge.svg)](https://codecov.io/gh/guillotinaweb/guillotina_linkintegrity/branch/master)
[![Python Versions](https://img.shields.io/pypi/pyversions/guillotina_linkintegrity.svg)](https://pypi.python.org/pypi/guillotina_linkintegrity/)
[![PyPi](https://img.shields.io/pypi/v/guillotina_linkintegrity.svg)](https://pypi.python.org/pypi/guillotina_linkintegrity)
[![License](https://img.shields.io/pypi/l/guillotina_linkintegrity.svg)](https://pypi.python.org/pypi/guillotina_linkintegrity/)


The package aims to provide link integrity support for Guillotina.

Features:
- Ability to check for linked content
- Automatically redirect requests when content is renamed or moved
- Manage aliases to content
- Translate resolveuid urls in text


## Dependencies

- Python >= 3.7
- Guillotina > 5
- PG/Cockroachdb with redis


## Installation

This example will use virtualenv:

```
  python -m venv .
  ./bin/pip install .[test]
```


## Running

Running Postgresql Server:

```
docker run --rm -e POSTGRES_DB=guillotina -e POSTGRES_USER=guillotina -p 127.0.0.1:5432:5432 --name postgres postgres:9.6
```


Most simple way to get running:

```
./bin/guillotina
```


# API

The package provides some high level APIs for interacting with content.

Working with linked content:

```python
import guillotina_linkintegrity as li

await li.get_links(ob)
await li.get_links_to(ob)
await li.add_links(ob, [ob2, ob3])
await li.remove_links(ob, [ob2, ob3])
await li.update_links_from_html(ob, content)
```

How about aliases:

```python
import guillotina_linkintegrity as li

await li.get_aliases(ob)
await li.add_aliases(ob, ['/foo/bar'])
await li.remove_aliases(ob, ['/foo/bar'])

# what about aliases from parents that might affect it?
await li.get_inherited_aliases(ob)
```

Translate uid linked content:

```python
import guillotina_linkintegrity as li

result = await li.translate_links(content)
```
