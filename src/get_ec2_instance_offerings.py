import json
from lib.ec2_describer import Ec2Describer

def main():
    ed = Ec2Describer()
    print(json.dumps(ed.describe_instance_type_offerings()))

if __name__ == "__main__":
    main()
