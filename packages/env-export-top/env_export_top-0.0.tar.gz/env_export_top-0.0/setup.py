"""
This package installs a pth file that will ensure that a $TOP environment
variable is set to the top of your development codebase before running any other
piece of python. The $TOP environment variable is set by searching the filesytem
for a `.top` file, starting from the .pth file itself and travsering parent
directories.

Demo::

    $ virtualenv tmpenv
    $ . tmpenv/bin/activate
    $ pip install export-top-var
    $ touch .top
    $ python -c 'import os; os.system("echo $TOP")'
    /my/current/path
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from distutils import log

from setuptools import setup
from setuptools.command.install import install as orig_install

PTH = '''\
import env_export_top; env_export_top.env_export_top()
'''

DOC = __doc__


class Install(orig_install):
    """
    default semantics for install.extra_path cause all installed modules to go
    into a directory whose name is equal to the contents of the .pth file.

    All that was necessary was to remove that one behavior to get what you'd
    generally want.
    """
    # pylint:disable=no-member,attribute-defined-outside-init,access-member-before-definition

    def initialize_options(self):
        orig_install.initialize_options(self)
        name = self.distribution.metadata.name

        contents = 'import sys; exec(%r)\n' % PTH
        self.extra_path = (name, contents)

    def finalize_options(self):
        orig_install.finalize_options(self)

        from os.path import relpath, join
        install_suffix = relpath(self.install_lib, self.install_libbase)
        if install_suffix == '.':
            log.info('skipping install of .pth during easy-install')
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            log.info(
                "will install .pth to '%s.pth'",
                join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                'unexpected install_suffix',
                self.install_lib, self.install_libbase, install_suffix,
            )


def main():
    """the entry point"""
    setup(
        name=str('env_export_top'),
        version='0.0',
        url="https://github.com/bukzor/python-env-export-top",
        license="MIT",
        author="Buck Evan",
        author_email="buck.2019@gmail.com",
        description="ensure that $TOP is always exported",
        long_description=DOC,
        zip_safe=False,
        classifiers=[
            # TODO: testing
            #'Programming Language :: Python :: 2.6',
            #'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'License :: OSI Approved :: MIT License',
        ],
        install_requires=[
            # TODO: break out a "pwdless" module, with HERE and TOP
        ],
        py_modules=['env_export_top'],
        cmdclass={
            'install': Install,
        },
        options={
            'bdist_wheel': {
                'universal': 1,
            },
        },
    )


if __name__ == '__main__':
    exit(main())
