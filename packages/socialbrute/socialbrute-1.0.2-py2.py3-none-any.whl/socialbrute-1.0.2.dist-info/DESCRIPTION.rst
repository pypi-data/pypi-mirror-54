===========
socialbrute
===========


.. image:: https://img.shields.io/pypi/v/socialbrute.svg
        :target: https://pypi.python.org/pypi/socialbrute

.. image:: https://img.shields.io/pypi/pyversions/socialbrute.svg
        :target: https://pypi.python.org/pypi/socialbrute

.. image:: https://readthedocs.org/projects/socialbrute/badge/?version=latest
        :target: https://socialbrute.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://travis-ci.com/5h4d0wb0y/socialbrute.svg?branch=master
        :target: https://travis-ci.com/5h4d0wb0y/socialbrute

.. image:: https://codecov.io/github/5h4d0wb0y/socialbrute/coverage.svg?branch=master
        :target: https://codecov.io/github/5h4d0wb0y/socialbrute?branch=master



SocialBrute attempts to crack a social network using a brute force dictionary attack.


* Free software: GNU General Public License v3
* Documentation: https://socialbrute.readthedocs.io.


Features
--------

* Browser supports proxy configuration
* Social network supported
        * Aol
        * Facebook
        * Gmail
        * Hotmail
        * Instagram
        * Twitter
        * VK
        * Yahoo


Credits
-------

This package was developed by @5h4d0wb0y_.

.. _@5h4d0wb0y: https://twitter.com/5h4d0wb0y


Stargazers over time
--------------------

.. image:: https://starchart.cc/5h4d0wb0y/socialbrute.svg
        :target: https://starchart.cc/5h4d0wb0y/socialbrute
        :alt: Stargazers over time

=======
History
=======

**unreleased**
**v1.0.3**

v1.0.2 (2019-10-27)
-------------------

* Added socialbrute tests for each module
* Check if the browser has been started on travis
* Added release-notes make command to generate history from the latest commits
* Added chromedriver installation and jobs environments on travis
* Fixed the installation of codecov in travis
* Removed unused imports and variables and conformed to the PEP 8 style guide
* Removed setuptools-changelog package, use only bump2version to change history
* Added installation of codecov in travis
* Added develop requirements
* Fixed phony and added other commands in makefile
* Fixed duplicate language in travis configuration

v1.0.1 (2019-10-21)
-------------------

* Added sudo and python language parameters
* Fixed packages inside setup.py
* Added --no-sandbox chrome option argument
* Fixed missing dependency

1.0.0 (2019-10-14)
------------------

* First release on PyPI.


