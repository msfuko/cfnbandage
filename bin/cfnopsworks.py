import argparse
import logging.config
import os
import sys
import json

sys.path.append(os.path.abspath("."))   #TODO: remove me
from cfnbandage.cfnbandage import CfnBandage
from cfnbandage.stack import StackSetting


def main(template, conf, patch_file):

    bandage = CfnBandage()

    # get config
    with open(conf, 'r') as f:
        config = f.read()
    config = json.loads(config)
    stack = StackSetting(**config)
    stack.validate()

    # get cloudformation template and create
    with open(template, 'r') as f:
        cfn_template = f.read()
    #cfn_stack_id = bandage.create_stack(stack.Stack['Region'], stack.Stack['Name'],
    #                                    cfn_template, stack.Stack['Parameters'])
    cfn_stack_id = "arn:aws:cloudformation:us-west-1:007588840706:stack/tt/8e536a10-5383-11e4-9e2a-5044330dbaa6"

    if patch_file:
        with open(patch_file, 'r') as f:
            patch_template = f.read()
        patch = json.loads(patch_template, parse_int=int)
        bandage.patch_bandage(stack.Stack['Region'], cfn_stack_id, patch, stack.Stack['Parameters'])



if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser(description='Cloudformation with OpsWorks')
    parser.add_argument("-t", "--template", type=str, help="cloudformation template", required=True)
    parser.add_argument("-c", "--config", type=str, help="config template", required=True)
    parser.add_argument("-p", "--patch", type=str, help="patch template", required=False)

    # logging
    logging.config.fileConfig(os.path.join(os.getcwd(), "conf", 'logging.ini'), disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    # parse args
    args = parser.parse_args()

    main(args.template, args.config, args.patch)

