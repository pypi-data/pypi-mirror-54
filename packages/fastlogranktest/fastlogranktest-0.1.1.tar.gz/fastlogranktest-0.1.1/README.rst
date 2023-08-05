===============================
fastlogranktest
===============================

Perform the Log-Rank-Test very fast

* Free software: BSD license

Features
--------

fastlogranktest.logrank_test(SAME_INPUT_AS_LOGRANK_FUNCTION_OF_LIFELINES_STATISTICS_PACKAGE)

fastlogranktest.multi_logrank_test(): 

Arguments same order as logrank_test() but list of lists of numbers for each instead of just a list of numbers.

Optional parameter: threadnumber 

Can set the number of threads manual.

For example: fastlogranktest.multi_logrank_test(..... , threadnumber = 12)

