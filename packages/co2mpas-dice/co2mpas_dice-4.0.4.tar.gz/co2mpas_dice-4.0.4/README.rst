.. _start-quick:

#################################################
co2mpas_dice: |co2mpas| Type Approval Mode Plugin
#################################################
|pypi_ver| |github_issues| |python_ver| |proj_license|

:release:       4.0.1
:date:          2019-10-21 01:40:00
:repository:    https://github.com/JRCSTU/DICE
:pypi-repo:     https://pypi.org/project/co2mpas_dice/
:docs:          http://co2mpas.readthedocs.io/
:wiki:          https://github.com/JRCSTU/DICE/wiki/
:download:      http://github.com/JRCSTU/DICE/releases/
:keywords:      scheduling, dispatch, dataflow, processing, calculation,
                dependencies, scientific, engineering, simulink, graph theory
:developers:    .. include:: AUTHORS.rst
:license:       `EUPL 1.1+ <https://joinup.ec.europa.eu/software/page/eupl>`_

.. _start-pypi:
.. _start-intro:

What is co2mpas_dice?
=====================
Schedula implements a intelligent function scheduler, which selects and
executes functions. The order (workflow) is calculated from the provided inputs
and the requested outputs. A function is executed when all its dependencies
(i.e., inputs, input domain) are satisfied and when at least one of its outputs
has to be calculated.

.. note::
   Schedula is performing the runtime selection of the **minimum-workflow** to
   be invoked. A workflow describes the overall process - i.e., the order of
   function execution - and it is defined by a directed acyclic graph (DAG).
   The **minimum-workflow** is the DAG where each output is calculated using the
   shortest path from the provided inputs. The path is calculated on the basis
   of a weighed directed graph (data-flow diagram) with a modified Dijkstra
   algorithm.


Installation
============
To install it use (with root privileges):

.. code-block:: console

    $ pip install co2mpas_dice

.. _end-quick:
.. _end-pypi:
.. _end-intro:
.. _start-badges:

.. |pypi_ver| image::  https://img.shields.io/pypi/v/co2mpas_dice.svg?
    :target: https://pypi.python.org/pypi/co2mpas_dice/
    :alt: Latest Version in PyPI

.. |python_ver| image:: https://img.shields.io/pypi/pyversions/co2mpas_dice.svg?
    :target: https://pypi.python.org/pypi/co2mpas_dice/
    :alt: Supported Python versions

.. |github_issues| image:: https://img.shields.io/github/issues/JRCSTU/DICE.svg?
    :target: https://github.com/JRCSTU/DICE/issues
    :alt: Issues count

.. |proj_license| image:: https://img.shields.io/badge/license-EUPL%201.1%2B-blue.svg?
    :target: https://raw.githubusercontent.com/JRCSTU/DICE/master/LICENSE.txt
    :alt: Project License
.. _end-badges:
