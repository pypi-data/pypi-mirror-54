========
lazyjson
========
|tests| |python|

**Encode existing JSON strings within new JSON documents efficiently...ish**

Sometimes you have some existing JSON snippets which you would like to include in a new JSON document or api response. This can be achieved cleanly but inefficiently by decoding the JSON first.

.. code-block:: python

    st = os.stat('tests/my.json')
    meta = {
        "size": st.st_size,
        "mtime": st.st_mtime,
        "content": json.load(open('tests/my.json'))
    }
    return json.dumps(meta)

The goal of this library is to provide an API which allows you to avoid ever decoding the snippet that's being included here.

JSONPassthroughEncoder
----------------------

This is a subclass of the standard lib's ``json.JSONEncoder`` and performs the magic enabling ``SafeJSON`` to work.

**WARNING**: **Blindly wrapping untrusted JSON strings could result in JSON injection attacks.** This library is not intended for everyday uses, but rather for complex proxy/file serving use cases where upstream is data you can trust. Please be careful, and only use when you're certain this is the correct tool for the job, and you trust any data you're embedding.

**WARNING**: **This class comes with massive performance penalties for encoding complex JSON structures from primitives.** The way in which this class is forced to work by the standard lib's json API is makes normal encoding inneficient, but the concept is otherwise simple and could be added to an existing C implementation trivially with no performance penalty.


*If the performance of this module is preventing you from using it but you have a valid use case please get in contact with me to collaborate on a C implementation.*

SafeJSON
--------

A wrapper for json-encoded strings which allows them to be output within a
JSON document by the ``JSONPassthroughEncoder`` without decoding first.

This is a subclass of ``LazyJSON``.

.. code-block:: python

    st = os.stat('my.json')
    doc = {
        "size": st.st_size,
        "mtime": st.st_mtime,
        "content": SafeJSON(open('my.json').read()),
    }
    return JSONPassthroughEncoder().encode(doc)

SafeJSONFile
------------

Like ``SafeJSON`` but for file-like objects instead of strings. This can be used for streaming extremely large embedded json documents without ever loading them fully into memory.

.. code-block:: python

    st = os.stat('my.json')
    doc = {
        "size": st.st_size,
        "mtime": st.st_mtime,
        "content": SafeJSONFile(open('my.json'), chunk_size=5000),
    }
    for t in JSONPassthroughEncoder().iterencode(doc):
        socket.write(t)

LazyJSON
--------

Like ``SafeJSON`` but **will not** be passed-through by ``JSONPassthroughEncoder`` classes.

This class can be used for untrusted JSON data for passing around your application and retaining the fact it's JSON-encoded, if you might only want to decode it sometimes.

Use the ``my_lazy_json.parse_json()`` method to parse the JSON.

After validation (usually of the parsed data) you can construct a ``SafeJSON`` object from this object to avoid re-encoding ``SafeJSON(my_lazy_json)``.

.. |tests| image:: https://github.com/willstott101/lazyjson/workflows/Tests/badge.svg
    :target: https://github.com/willstott101/lazyjson/actions
.. |python| image:: https://img.shields.io/badge/python-3.5+-blue.svg