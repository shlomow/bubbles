![build status](https://api.travis-ci.org/shlomow/bubbles.svg?branch=master)
![coverage](https://codecov.io/gh/shlomow/bubbles/branch/master/graph/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/bubbles-advanced-system-design/badge/?version=latest)](https://bubbles-advanced-system-design.readthedocs.io/en/latest/?badge=latest)

# Bubbles

## Introduction

This package supports a Brain Computer Interface — imaginary hardware that can read minds, and upload snapshots of cognitions.

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/shlomow/bubbles.git
    ...
    $ cd bubbles/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [foobar] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

In order to upload snapshots to the server, you can use a cli:

```sh
$ python -m bubbles.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
```

Or, you can use the python interpreter:
```python
>>> from bubbles.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```

In order to run the server, you can use a cli:

```sh
$ python -m bubbles.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
```

Or, you can use the python interpreter:
```python
>>> from cortex.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
```

In order to run the parser, you can use a cli:

```sh
$ python -m bubbles.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```

Or, you can use the python interpreter:
```python
>>> from bubbles.parsers import run_parser
>>> data = … 
>>> result = run_parser('pose', data)
```

To run the parser as a service use the following cli:

```sh
$ python -m bubbles.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```

In order to run the saver, you can use a cli:

```sh
$ python -m bubbles.saver save                     \
      -d/--database 'postgresql://127.0.0.1:5432' \
     'pose'                                       \
     'pose.result'
```

Or, you can use the python interpreter:
```python
>>> from bubbles.saver import Saver
>>> saver = Saver(database_url)
>>> data = …
>>> saver.save('pose', data)
```

To run the saver as a service use the following cli:

```sh
$ python -m bubbles.saver run-saver  \
      'postgresql://127.0.0.1:5432' \
      'rabbitmq://127.0.0.1:5672/'
```

In order to run the api server, you can use a cli:

```sh
$ python -m bubbles.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'postgresql://127.0.0.1:5432'
```

Or, you can use the python interpreter:
```python
>>> from cortex.api import run_api_server
>>> run_api_server(
...     host = '127.0.0.1',
...     port = 5000,
...     database_url = 'postgresql://127.0.0.1:5432',
... )
```

The api is reflected by the following cli:
```sh
$ python -m cortex.cli get-users
…
$ python -m cortex.cli get-user 1
…
$ python -m cortex.cli get-snapshots 1
…
$ python -m cortex.cli get-snapshot 1 2
…
$ python -m cortex.cli get-result 1 2 'pose'
…
```

You can also use a graphical user interface to consume the database:
```sh
$ python -m bubbles.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
```

Or, using the python interpreter:
```python
>>> from bubbles.gui import run_server
>>> run_server(
...     host = '127.0.0.1',
...     port = 8080,
...     api_host = '127.0.0.1',
...     api_port = 5000,
... )
```