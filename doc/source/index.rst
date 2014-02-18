.. buildbot-haskell documentation master file, created by
   sphinx-quickstart on Tue Feb 18 11:54:04 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

buildbot-haskell
================

.. toctree::
   :maxdepth: 2

.. automodule:: buildbot_haskell.cabal
   :members:
   :undoc-members:

Using a sandbox
---------------

.. note::
  For sandbox support, cabal-install 1.19 or newer is required.

In order to use a sandbox, provide the ``sandbox`` argument to the ``Cabal``
constructor, for example:

::

  cabal = Cabal(sandbox=".")

to use a sandbox right in the build directory or

::

  cabal = Cabal(sandbox="my/sandbox")

to use a sandbox in a subdirectory.

All cabal commands from a sandboxed ``Cabal`` instance will use that sandbox
automatically, regardless of which directory they are invoked from.

If the sandbox doesn't exist yet, call :py:meth:`~buildbot_haskell.cabal.Cabal.sandbox_init` to create it.

It will also create the sandbox directory (such as ``my/sandbox`` in the example
above) if it doesn't exist.

``sandbox_delete`` will destroy the sandbox 

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

