#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class InstallCommand(install):
    user_options = install.user_options + [
        ('orig', 'o', 'Use original code')
    ]

    def initialize_options(self):
        super().initialize_options()
        self.orig = 0

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        if self.orig or ORIG:
            self.distribution.packages = find_packages('src')
            self.distribution.package_dir = {'': 'src'}
        print(self.distribution.packages, self.distribution.package_dir)
        super().run()


ORIG = bool(os.environ.get('SE_CODE_ORIG', False))

setup(
    name='se_code',
    packages=find_packages('changes'),
    package_dir={'': 'changes'},
    cmdclass={
        'install': InstallCommand,
    }
)
