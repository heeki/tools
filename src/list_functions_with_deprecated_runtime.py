import json
from lib.lambda_describer import LambdaDescriber

DEPRECATED_RUNTIME_IDENTIFIERS = [
  "python3.6",
  "python2.7",
  "dotnetcore2.1",
  "ruby2.5",
  "nodejs10.x",
  "nodejs8.10",
  "nodejs4.3",
  "nodejs6.10",
  "dotnetcore1.0",
  "dotnetcore2.0",
  "nodejs4.3-edge",
  "nodejs"
]

def main():
    ld = LambdaDescriber()
    # output = ld.list_functions(online=True)
    # output = ld.list_functions(online=False)
    output = ld.list_functions_in_runtime_list(DEPRECATED_RUNTIME_IDENTIFIERS, online=False)
    print(json.dumps(output))

if __name__ == "__main__":
    main()
