===============================
fastlogranktest
===============================

.. image:: https://img.shields.io/travis/ga63nep/fastlogranktest.svg
        :target: https://travis-ci.org/ga63nep/fastlogranktest

.. image:: https://coveralls.io/repos/ga63nep/fastlogranktest/badge.svg?branch=master
   :target: https://coveralls.io/r/ga63nep/fastlogranktest?branch=master 

.. image:: https://ci.appveyor.com/api/projects/status/fuu825yp9ep83tgq/branch/master?svg=true
   :target: https://ci.appveyor.com/api/projects/status/fuu825yp9ep83tgq


Perform the Log-Rank-Test very fast

* Free software: BSD license
* Documentation: https://fastlogranktest.readthedocs.org.

Features
--------

Call funtions:

cpplogrank.logrank_test(SAME_INPUT_AS_LOGRANK_FUNCTION_OF_LIFELINES_STATISTICS_PACKAGE)

cpplogrank.multi_logrank_test():
Arguments same order as logrank_test() but list of lists of numbers for each instead of just a list of numbers.

Optional parameter: threadnumber
Can set the number of threads manual
For example: cpplogrank.multi_logrank_test(..... , threadnumber = 12)

