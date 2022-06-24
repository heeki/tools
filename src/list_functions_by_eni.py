import json
from lib.lambda_describer import LambdaDescriber

def main():
    ld = LambdaDescriber()
    # output = ld.list_functions()
    output = ld.list_functions_by_eni(online=True)
    print(json.dumps(output))

if __name__ == "__main__":
    main()
