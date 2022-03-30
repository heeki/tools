include etc/environment.sh

list_functions_by_layer:
	python3 src/list_functions_by_layer.py | jq
analyze_sf_execution:
	python3 src/analyze_sf_execution.py --exec_arn ${SF_EXEC_ARN} | jq
get_code_storage:
	python3 src/get_code_storage.py | jq