import json
from lib.lambda_describer import LambdaDescriber

def main():
    ld = LambdaDescriber()
    # print(json.dumps(ld.get_concurrency_limits()))
    print(json.dumps(ld.get_code_storage()))

if __name__ == "__main__":
    main()
