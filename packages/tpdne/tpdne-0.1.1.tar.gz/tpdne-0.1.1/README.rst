tpdne
#####

.. image:: https://travis-ci.com/carl-mundy/tpdne.svg?branch=master
    :target: https://travis-ci.com/carl-mundy/tpdne
    :alt: Build Status
.. image:: https://coveralls.io/repos/github/carl-mundy/tpdne/badge.svg?branch=master
    :target: https://coveralls.io/github/carl-mundy/tpdne?branch=master
    :alt: Code Coverage
.. image:: https://api.codeclimate.com/v1/badges/494ceedc7d595e8991fd/maintainability
   :target: https://codeclimate.com/github/carl-mundy/tpdne/maintainability
   :alt: Maintainability

Quickstart
==========

tpdne is available on PyPI and can be installed with `pip <https://pip.pypa.io>`_.

.. code-block:: console

    $ pip install tpdne

After installing tpdne you can use it like any other Python module.

Here is a simple example:

.. code-block:: python

    import tpdne
    image = tpdne.tpdne_base64()

Or, if being used within a Jupyter Notebook:

.. code-block:: python

    import tpdne
    from IPython.display import Image, Markdown

    Image(data=tpdne.tpdne_bytes())
    Markdown('<img src="data:image/png;base64,{}" />'.format(tpdne.tpdne_base64()))
