import boto3
import json
from lib.encoders import DateTimeEncoder

class SfnDescriber:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client("stepfunctions")

    # helper functions
    def describe_execution(self, exec_arn):
        response = self.client.describe_execution(
            executionArn = exec_arn
        )
        output = response
        return output

    def _get_execution_history(self, exec_arn, next_token=None):
        if next_token is None:
            response = self.client.get_execution_history(
                executionArn=exec_arn,
                maxResults=100
            )
        else:
            response = self.client.get_execution_history(
                executionArn=exec_arn,
                maxResults=100,
                nextToken=next_token
            )
        return response

    def get_execution_history(self, exec_arn):
        history = []
        response = self._get_execution_history(exec_arn)
        history.extend(response["events"])
        # while "NextToken" in response:
        #     response = self._get_execution_history(exec_arn, next_token=response["NextToken"])
        #     history.extend(response["events"])
        return history

    def print_history(self, history):
        for event in history:
            print(json.dumps(event, cls=DateTimeEncoder))

    def analyze_history(self, history):
        timestamps = {}
        start_to_scheduled_mapping = {}
        for event in history:
            if event["type"] == "LambdaFunctionScheduled":
                timestamps[event["id"]] = {}
                timestamps[event["id"]]["scheduled"] = event["timestamp"]
            elif event["type"] == "LambdaFunctionStarted":
                start_id = event["previousEventId"]
                start_to_scheduled_mapping[event["id"]] = start_id
                timestamps[start_id]["started"] = event["timestamp"]
            elif event["type"] == "LambdaFunctionSucceeded":
                start_id = start_to_scheduled_mapping[event["previousEventId"]]
                timestamps[start_id]["succeeded"] = event["timestamp"]

        scheduling_overhead = 0
        fn_total = 0
        for eid in timestamps:
            fn_scheduling = (timestamps[eid]["started"] - timestamps[eid]["scheduled"]).total_seconds()
            fn_duration = (timestamps[eid]["succeeded"] - timestamps[eid]["started"]).total_seconds()
            scheduling_overhead += fn_scheduling
            fn_total += fn_duration
            timestamps[eid]["scheduling_duration_s"] = fn_scheduling
            timestamps[eid]["execution_duration_s"] = fn_duration

        elapsed_duration = (history[-1]["timestamp"] - history[0]["timestamp"]).total_seconds()
        output = {
            "lambda_timestamps": timestamps,
            "elapsed_duration_s": elapsed_duration,
            "scheduling_overhead_s": scheduling_overhead,
            "serial_fn_total_s": fn_total
        }
        print(json.dumps(output, cls=DateTimeEncoder))
        return output
