import argparse
import logging.config
import os
import sys
import json

sys.path.append(os.path.abspath("."))   #TODO: remove me
from cfnbandage.cfnbandage import CfnBandage
from cfnbandage.stack import StackSetting


def main(template, cfn_stack_id, conf, patch_file):

    bandage = CfnBandage()

    # get config
    with open(conf, 'r') as f:
        config = f.read()
    config = json.loads(config)
    stack = StackSetting(**config)
    stack.validate()

    if template:
        # get cloudformation template and create
        with open(template, 'r') as f:
            cfn_template = f.read()
        cfn_stack_id = bandage.create_stack(stack.Stack['Region'], stack.Stack['Name'],
                                            cfn_template, stack.Stack['Parameters'])
    elif cfn_stack_id:
        pass
    else:
        raise ValueError("Cannot identify CloudFormation Stack ID")

    logger.debug("CloudFormation Stack Id %s", cfn_stack_id)
    if patch_file:
        with open(patch_file, 'r') as f:
            patch_template = f.read()
        patch = json.loads(patch_template, parse_int=int)
        bandage.patch_bandage(stack.Stack['Region'], cfn_stack_id, patch, stack.Stack['Parameters'])



if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser(description='Cloudformation with OpsWorks')
    parser.add_argument("-t", "--template", type=str, help="cloudformation template", required=False)
    parser.add_argument("-i", "--id", type=str, help="cloudformation stack id", required=False)
    parser.add_argument("-c", "--config", type=str, help="config template", required=True)
    parser.add_argument("-p", "--patch", type=str, help="patch template", required=False)

    # logging
    logging.config.fileConfig(os.path.join(os.getcwd(), "conf", 'logging.ini'), disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    # parse args
    args = parser.parse_args()

    main(args.template, args.id, args.config, args.patch)

