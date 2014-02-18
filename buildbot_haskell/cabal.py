from buildbot.steps.shell import ShellCommand
from itertools import chain
import pipes

def union(x,y):
    """Right-biased dictionary union"""
    return dict(x.items() + y.items())

class Cabal:
    """
    An object of the :py:class:`Cabal` class is used to issue ``cabal``
    commands.

    Methods of the class accept a number of configuration parameters that are
    described in the corresponding section of the documentation. The default
    values can be also supplied when an object is created. Example: ::

            cabal = Cabal(sandbox=".", optimization=1)
            cabal.install("ansi-terminal", optimization=0, jobs=2)

    """
    default_config = { 'sandbox': None, 'optimization': 0, 'jobs': 1 }

    def __init__ (self, **config):
        self.config = union(Cabal.default_config, config)

    def __sandboxOpt(self, config):
        sandbox = union(self.config, config)['sandbox']
        if not sandbox is None:
            yield "--sandbox-config-file={0}/cabal.sandbox.config".format(sandbox)

    def __optimizationOpt(self, config):
        yield "--ghc-option=-O{0}".format(union(self.config, config)['optimization'])

    def __jobsOpt(self, config):
        yield "-j{0}".format(union(self.config, config)['jobs'])

    def __allOpts(self, config):
        return chain(self.__sandboxOpt(config), self.__optimizationOpt(config), self.__jobsOpt(config))

    def update(self, **config):
        """Run ``cabal update``"""
        return ShellCommand(
            name="cabal update",
            description="Downloading the latest package list",
            command=["cabal", "update"],
            **config
        )

    def install(self, package, **config):
        """Run ``cabal install package``"""
        return ShellCommand(
            name="cabal install {0}".format(package),
            command=list(chain(["cabal", "install", package], self.__allOpts(config))),
            **config
        )

    def __get_sandbox(self, config):
        sandbox = union(self.config, config)['sandbox']
        if sandbox is None:
            raise ValueError("sandbox is not defined")
        return sandbox

    def sandbox_init(self, **config):
        """
        Run ``cabal sandbox init``.

        If the sandbox directory doesn't exist, it will be created.

        .. note::
          ``sandbox_init`` probably won't work with a Windows slave. Patches are welcome.
        """
        sandbox = self.__get_sandbox(config)
        return ShellCommand(
            name="cabal sandbox init",
            description="Initializing sandbox at {0}".format(sandbox),
            workdir=".",
            command="mkdir -p {0} && cd {0} && cabal sandbox init".format(pipes.quote(sandbox))
        )
    def sandbox_delete(self, **config):
        """
        Run ``cabal sandbox delete`` in the sandbox directory specified during the
        :py:class:`Cabal` instance creation.

        The directory itself is not removed.
        """
        sandbox = self.__get_sandbox(config)
        return ShellCommand(
            name="cabal sandbox delete",
            description="Deleting sandbox at {0}".format(sandbox),
            workdir=sandbox,
            command=["cabal","sandbox","delete"]
        )
