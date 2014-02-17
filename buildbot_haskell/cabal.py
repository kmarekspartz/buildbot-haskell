from buildbot.steps.shell import ShellCommand
from itertools import chain

class Cabal:
    def __init__ (self, sandbox = None, optimization = 0, jobs = 1):
        self.sandbox = sandbox
        self.optimization = optimization
        self.jobs = jobs

    def sandboxOpt(self):
        if not self.sandbox is None:
            yield "--sandbox-config-file={0}/cabal.sandbox.config".format(self.sandbox)

    def optimizationOpt(self):
        yield "--ghc-option=-O{0}".format(self.optimization)

    def jobsOpt(self):
        yield "-j{0}".format(self.jobs)

    def allOpts(self):
        return chain(self.sandboxOpt(), self.optimizationOpt(), self.jobsOpt())

    def update(self, **kwargs):
        return ShellCommand(
            name="cabal update",
            description="Downloading the latest package list",
            command=["cabal", "update"],
            **kwargs
        )

    def install(self, package, **kwargs):
        return ShellCommand(
            name="cabal install {0}".format(package),
            command=list(chain(["cabal", "install", package], self.allOpts())),
            **kwargs
        )
