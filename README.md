## Overview
Repository for miscellaneous tools on AWS.

## Description
`list_functions_by_layer.py`: outputs json document which keys by layer version and lists an array of functions within that account/region
`analyze_sf_execution.py`: pulls step functions execution history and outputs execution time for each Lambda state transition
`get_code_storage_limit.py`: gets the account code storage limit