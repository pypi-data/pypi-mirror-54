wlc
===

`Weblate`_ commandline client using `Weblate's REST API`_.

.. image:: https://travis-ci.com/WeblateOrg/wlc.svg?branch=master
    :target: https://travis-ci.com/WeblateOrg/wlc
    :alt: Build Status

.. image:: https://ci.appveyor.com/api/projects/status/e9a8n9qhvd6ulibw/branch/master?svg=true
    :target: https://ci.appveyor.com/project/nijel/wlc/branch/master
    :alt: Build status

.. image:: https://codecov.io/github/WeblateOrg/wlc/coverage.svg?branch=master
    :target: https://codecov.io/github/WeblateOrg/wlc?branch=master
    :alt: Code coverage

.. image:: https://img.shields.io/pypi/v/wlc.svg
    :target: https://pypi.org/project/wlc/
    :alt: PyPI package

.. image:: https://hosted.weblate.org/widgets/weblate/-/svg-badge.svg
    :alt: Translation status
    :target: https://hosted.weblate.org/engage/weblate/?utm_source=widget

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :alt: Documentation
    :target: https://docs.weblate.org/en/latest/wlc.html

Installation
------------

Install using pip:

.. code-block:: sh

    pip3 install wlc

Sources are available at <https://github.com/WeblateOrg/wlc>.

Usage
-----

Please see `Weblate documentation`_ for more complete documentation.

Command line usage:

.. code-block:: sh

    wlc list-projects
    wlc list-components
    wlc list-translations
    wlc list-languages
    wlc show
    wlc ls
    wlc commit
    wlc push
    wlc pull
    wlc repo
    wlc stats
    wlc lock
    wlc unlock
    wlc lock-status
    wlc download
    wlc upload

Configuration is stored in ``~/.config/weblate``:

.. code-block:: ini

    [weblate]
    url = https://hosted.weblate.org/api/

    [keys]
    https://hosted.weblate.org/api/ = APIKEY

.. _Weblate's REST API: https://docs.weblate.org/en/latest/api.html
.. _Weblate documentation: https://docs.weblate.org/en/latest/wlc.html
.. _Weblate: https://weblate.org/
