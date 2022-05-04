import argparse
import json
from lib.ec2_describer import Ec2Describer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="instance type")
    args = ap.parse_args()

    ed = Ec2Describer()
    print(json.dumps(ed.describe_instance_type_offerings(args.type)))

if __name__ == "__main__":
    main()
