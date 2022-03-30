import argparse
from lib.sf_describer import SfnDescriber

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exec_arn", required=True, help="execution arn")
    args = ap.parse_args()
    sfd = SfnDescriber()
    history = sfd.get_execution_history(args.exec_arn)
    # sfd.print_history(history)
    analysis = sfd.analyze_history(history)

if __name__ == "__main__":
    main()
