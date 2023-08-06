# Copyright DataStax, Inc.
#
# The full license terms are available at http://www.datastax.com/terms/datastax-dse-driver-license-terms

from __future__ import print_function

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
from distutils.cmd import Command

exec(open('dse_graph/_version.py').read())

long_description = ""
with open("README.rst") as f:
    long_description = f.read()


class DocCommand(Command):

    description = "generate documentation"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = "docs/_build/%s" % __version__
        mode = "html"

        try:
            os.makedirs(path)
        except:
            pass

        import os
        import subprocess
        try:
            output = subprocess.check_output(
                ["sphinx-build", "-b", mode, "docs", path],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("Documentation step '%s' failed: %s: %s" % (mode, exc, exc.output))
        else:
            print(output)

        print("")
        print("Documentation step '%s' performed, results here:" % mode)
        print("   file://%s/%s/index.html" % (os.path.dirname(os.path.realpath(__file__)), path))

dependencies = ['dse-driver>=2.3.0,<2.12', 'gremlinpython==3.3.4', 'six>=1.6']

setup(
    name='dse-graph',
    version=__version__,
    description='DataStax Enterprise extension for graph',
    long_description=long_description,
    packages=["dse_graph"],
    keywords='cassandra,dse,graph,tinkerpop',
    include_package_data=True,
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license="DataStax DSE Driver License http://www.datastax.com/terms/datastax-dse-driver-license-terms",
    cmdclass={'doc': DocCommand})
