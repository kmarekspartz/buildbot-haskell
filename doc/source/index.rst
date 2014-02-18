.. buildbot-haskell documentation master file, created by
   sphinx-quickstart on Tue Feb 18 11:54:04 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

buildbot-haskell
================

.. toctree::
   :maxdepth: 2

About
-----

buildbot-haskell is an add-on package for `buildbot <http://buildbot.net/>`_
that simplifies building haskell packages.

If you are new to buildbot, please see the `tutorial
<http://docs.buildbot.net/0.8.8/tutorial/index.html>`_.

Example
-------

Here's a build factory that installs a package from hackage: ::

  cabal = Cabal(sandbox=".")
  factory = BuildFactory([cabal.update()
                        , cabal.sandbox_init()
                        , cabal.install(pkg)
                        , cabal.sandbox_delete()
                        ])


Using a sandbox
---------------

.. note::
  For sandbox support, cabal-install 1.18 or newer is required.

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


API documentation
-----------------

.. autoclass:: buildbot_haskell.cabal.Cabal
   :members:

Configuration options
---------------------


:py:obj:`optimization`
  controls the ``-O`` flag passed to GHC (e.g.  ``optimization=1`` will
  result in ``-O1``).

  default: 0

:py:obj:`jobs`
  the number of jobs (threads) used for compilation. It corresponds to
  cabal's ``-j`` flag.

  default: 1

:py:obj:`sandbox`
  specifies an optional sandbox directory. If it is not :py:const:`None`, all
  cabal commands will be sandboxed.

  default: :py:obj:`None`
