pybwtool
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python wrapper for the `bwtool library <https://github.com/CRG-Barcelona/bwtool>`_.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install pybwtool

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|


Getting started
----------------------------------------------
At the time of writing, the package includes just two methods from `bwtool <https://github.com/CRG-Barcelona/bwtool>`_. If you need more, you are more than welcome
to open a pull request adding the new feature or opening a new issue with the request. In the second case I'll work on it when I'll get the time.

Extract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The extract method returns a pandas Dataframe with the data from the regions of a bed file extracted from the given bigwig.

.. code:: python

    from pybwtool import extract

    df = extract("path/to/my/bed", "path/to/my/bigwig")

Extract mean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The extract_mean method, similarly to the extract methon, returns a pandas Dataframe with the mean of the data from the regions of a bed file extracted from the given bigwig.

.. code:: python

    from pybwtool import extract_mean

    df = extract_mean("path/to/my/bed", "path/to/my/bigwig")


Common fixes for getting bwtool to work
----------------------------------------------
- `For when the installation of bwtool gets stuck <https://github.com/CRG-Barcelona/bwtool/issues/65>`_
- `For when the installation of libbeato (a required library) gets stuck <https://github.com/CRG-Barcelona/libbeato/issues/6>`_



.. |travis| image:: https://travis-ci.org/LucaCappelletti94/pybwtool.png
   :target: https://travis-ci.org/LucaCappelletti94/pybwtool
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_pybwtool&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_pybwtool
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/pybwtool/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/pybwtool?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/pybwtool.svg
    :target: https://badge.fury.io/py/pybwtool
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/pybwtool
    :target: https://pepy.tech/badge/pybwtool
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/6f79fce7cb144f509ed584af3f950ab8
    :target: https://www.codacy.com/manual/LucaCappelletti94/pybwtool?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/pybwtool&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/68b5e35660142727406a/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/pybwtool/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/68b5e35660142727406a/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/pybwtool/test_coverage
    :alt: Code Climate Coverate