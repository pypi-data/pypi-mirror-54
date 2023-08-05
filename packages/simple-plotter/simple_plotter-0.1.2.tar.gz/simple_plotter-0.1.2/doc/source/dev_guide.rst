Developer documentation
=======================

Package versioning
------------------

setuptools_scm is used to fetch the version strings from git tags/commits automatically.

Building conda packages
-----------------------

There will probably be no need to update the meta.yaml manually.
conda-build's jinja templating functionality is used in meta.yaml to fetch the package information from setup.py (except
for the package version).

Since setuptools_scm is used, there is no version argument, that can be imported with the load_setup_py_data function
in meta.yaml.

Therefore **conda packages should be built using the build_conda_package.sh shell script.**

This script first reads the (auto-generated) version from setup.py and passes it to an environment variable, which is
used in the meta.yaml.

Project documentation
---------------------

Documentation sources for sphinx are stored in the doc/ folder.

When commits to master are pushed to the gitlab repository the documentation is automatically generated on readthedocs:

https://simple-plotter.readthedocs.io/latest

If tags are pushed documentation will be generated for

https://simple-plotter.readthedocs.io/stable