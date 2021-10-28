import boto3
import json
import sys
from enum import Enum

class LayerOptions(Enum):
    BASE = 1
    LATEST = 2
    ALL_VERSIONS = 3

class LambdaDescriber:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client("lambda")

    # helper functions
    def _list_layer_versions(self, layer):
        response = self.client.list_layer_versions(
            LayerName=layer
        )
        return response["LayerVersions"]

    def _list_functions_paginated(self, next_marker=None):
        if next_marker is None:
            response = self.client.list_functions()
        else:
            response = self.client.list_functions(
                Marker=next_marker
            )
        return response

    # main functions
    def list_layers(self, desired=None):
        response = self.client.list_layers()
        output = []
        for layer in response["Layers"]:
            if desired == LayerOptions.BASE:
                layer_arn = layer["LayerArn"]
            elif desired == LayerOptions.LATEST:
                layer_arn = layer["LatestMatchingVersion"]["LayerVersionArn"]
            elif desired == LayerOptions.ALL_VERSIONS:
                layer_arn = layer["LayerArn"]
                versions = self._list_layer_versions(layer_arn)
                for version in versions:
                    output.append(version["LayerVersionArn"])
            else:
                sys.exit(1)
            output.append(layer_arn)
        return output

    def list_functions(self, next_marker=None, online=False):
        fns = []
        if online:
            response = self._list_functions_paginated()
            fns.extend(response["Functions"])
            while "NextMarker" in response:
                response = self._list_functions_paginated(next_marker=response["NextMarker"])
                fns.extend(response["Functions"])
        else:
            with open("tmp/list_functions.json") as f:
                fns = json.load(f)
        return fns

    def list_functions_by_layer(self, online=False):
        layers = self.list_layers(LayerOptions.ALL_VERSIONS)
        fns = self.list_functions(online=online)

        output = {}
        for in_scope in layers:
            output[in_scope] = []
            for fn in fns:
                if "Layers" in fn:
                    for layer in fn["Layers"]:
                        if in_scope == layer["Arn"]:
                            output[in_scope].append(fn["FunctionName"])
        return output

def main():
    ld = LambdaDescriber()
    # output = ld.list_layers(LayerOptions.BASE)
    # output = ld.list_layers(LayerOptions.LATEST)
    # output = ld.list_layers(LayerOptions.ALL_VERSIONS)
    # output = ld.list_functions()
    output = ld.list_functions_by_layer(online=True)
    print(json.dumps(output))

if __name__ == "__main__":
    main()
