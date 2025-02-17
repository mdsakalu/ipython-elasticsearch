=====================
ipython-elasticsearch
=====================

:Author: Gilad Raphaelli, http://g.raphaelli.com

Adds %elasticsearch magic.

Usage
-----

.. code:: ipython3

    %elasticsearch?

.. parsed-literal::

    Docstring:
    ::

      %elasticsearch [-o OUTPUT] [base_url]

    elasticsearch line magic

    positional arguments:
      base_url              Elasticsearch URL.

    optional arguments:
      -o OUTPUT, --output OUTPUT
                            save result to variable of this name

Examples
--------

.. image:: notebook.png
   :height: 1009 px
   :width: 1103 px
   :scale: 100%
   :alt: notebook example
   :align: center
   :target: Learn%20Elasticsearch%20with%20Jupyter.ipynb

.. code:: ipython3

    In [1]: %load_ext elasticsearch

    In [2]: %%elasticsearch
            PUT twitter
            {
              "mappings": {
                "tweet": {
                  "properties": {
                    "message": {
                      "type": "string"
                    }
                  }
                }
              }
            }

    Out[2]: {'acknowledged': True}



Defaults endpoint http://localhost:9200:

.. code:: ipython3

    In [3]: %elasticsearch
            Using: http://localhost:9200/

Configure endpoint for the whole notebook:

.. code:: ipython3

    In [4]: %elasticsearch http://my.host.es:1234/
            Using: http://my.host.es:1234/

    In [5]: %elasticsearch
            Using: http://my.host.es:1234/

    In [6]: %elasticsearch http://localhost:9200/
            Using: http://localhost:9200/

Use a different endpoint for one cell:

.. code:: ipython3

    In [7]: %%elasticsearch http://my.host.es:1234/
            GET /

    Out[7]: {'cluster_name': 'elasticsearch',
             'name': 'my.host.es',
             'tagline': 'You Know, for Search',
             'version': {'build_hash': 'de54438d6af8f9340d50c5c786151783ce7d6be5',
             'build_snapshot': False,
             'build_timestamp': '2015-10-22T08:09:48Z',
             'lucene_version': '5.2.1',
             'number': '2.0.0'}}

    In [8]: %elasticsearch
            Using: http://localhost:9200/

Save result to a local variable:

.. code:: ipython3

    In [9]: %%elasticsearch http://my.host.es:1234/ -o foo
            GET /

    Out[9]: {'cluster_name': 'elasticsearch',
             'name': 'my.host.es',
             'tagline': 'You Know, for Search',
             'version': {'build_hash': 'de54438d6af8f9340d50c5c786151783ce7d6be5',
             'build_snapshot': False,
             'build_timestamp': '2015-10-22T08:09:48Z',
             'lucene_version': '5.2.1',
             'number': '2.0.0'}}

    In[10]: print(foo['tagline'])
            You Know, for Search

Installing
----------

Install the lastest release with::

    pip install ipython-elasticsearch

or clone from https://github.com/graphaelli/ipython-elasticsearch and::

    cd ipython-elasticsearch
    python setup.py install

Development
-----------

https://github.com/graphaelli/ipython-elasticsearch

Todo
----

- configurables
  - default elasticsearch endpoint
  - renderjson styles
- appropriate default output in console
- contextual help

Credit
------

- https://github.com/catherinedevlin/ipython-sql for serving as a template
- http://caldwell.github.io/renderjson/ for the collapsable JSON rendering
