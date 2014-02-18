from buildbot.steps.shell import ShellCommand
from itertools import chain
import pipes

class Cabal:
    """
    An object of the :py:class:`Cabal` class is used to issue ``cabal`` commands
    with consistent settings. The settings themselves are specified when the
    object is created, e.g.

    ::
            cabal = Cabal(sandbox=".", optimization=1, jobs=4)

    """
    def __init__ (self, sandbox = None, optimization = 0, jobs = 1):
        self.sandbox = sandbox
        self.optimization = optimization
        self.jobs = jobs

    def __sandboxOpt(self):
        if not self.sandbox is None:
            yield "--sandbox-config-file={0}/cabal.sandbox.config".format(self.sandbox)

    def __optimizationOpt(self):
        yield "--ghc-option=-O{0}".format(self.optimization)

    def __jobsOpt(self):
        yield "-j{0}".format(self.jobs)

    def __allOpts(self):
        return chain(self.__sandboxOpt(), self.__optimizationOpt(), self.__jobsOpt())

    def update(self, **kwargs):
        """Run ``cabal update``"""
        return ShellCommand(
            name="cabal update",
            description="Downloading the latest package list",
            command=["cabal", "update"],
            **kwargs
        )

    def install(self, package, **kwargs):
        """Run ``cabal install package``"""
        return ShellCommand(
            name="cabal install {0}".format(package),
            command=list(chain(["cabal", "install", package], self.__allOpts())),
            **kwargs
        )

    def __sandbox_check(self):
        if self.sandbox is None:
            raise ValueError(
                "sandbox_init: sandbox is not defined.\n"
                "Provide the sandbox argument when creating a Cabal object")

    def sandbox_init(self, **kwargs):
        """
        Run ``cabal sandbox init`` in the sandbox directory specified during the
        :py:class:`Cabal` instance creation

        If the sandbox directory doesn't exist, it will be created.

        .. note::
          ``sandbox_init`` probably won't work with a Windows slave. Patches are welcome.
        """
        self.__sandbox_check()
        return ShellCommand(
            name="cabal sandbox init",
            description="Initializing sandbox at {0}".format(self.sandbox),
            command="mkdir -p {0} && cd {0} && cabal sandbox init".format(pipes.quote(self.sandbox))
        )
    def sandbox_delete(self, **kwargs):
        """
        Run ``cabal sandbox delete`` in the sandbox directory specified during the
        :py:class:`Cabal` instance creation.

        The directory itself is not removed.
        """
        self.__sandbox_check()
        return ShellCommand(
            name="cabal sandbox delete",
            description="Deleting sandbox at {0}".format(self.sandbox),
            workdir=self.sandbox,
            command=["cabal","sandbox","delete"]
        )
