import json,argparse
from .tfcloud import TFCloud

def parse_args():
    parser = argparse.ArgumentParser(description='Sync tfvars file with tfcloud')
    parser.add_argument(
        '-w',
        '--workspace',
        type=str,
        help='tfcloud workspace name',
        required=True
    )
    parser.add_argument(
        '-o',
        '--organization',
        type=str,
        help='tfcloud organization name',
        required=True
    )
    return parser.parse_args()


def main():
    args = parse_args()
    tfcloud = TFCloud()
    workspace_id = tfcloud.get_workspace_id(args.organization,args.workspace)
    outputs = tfcloud.get_current_state_outputs(workspace_id)
    print(json.dumps(outputs))
