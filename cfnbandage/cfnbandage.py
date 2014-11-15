import logging

from . import AWSObject
from lib.cloudformation import CloudFormation
from lib.connection import Connection
from .opsworks import LoadBasedAutoScalingConfigurations, Instance

# use for checking we support it before you call eval
SUPPORTED_BANDAGE = {"Opsworks": ["Instance", "LoadBasedAutoScalingConfigurations"]}

# change the special region if it listed in SUPPORTED_REGION,
# some service is only supported in specific region
SUPPORTED_REGION = {"Opsworks": "us-east-1"}


class CfnBandage():

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def create_stack(self, region, name, template, parameters):
        self.logger.debug("meeh")
        connection = Connection("cloudformation", region)
        self.logger.debug("conn ok")
        cfn = CloudFormation(connection=connection.new_connection())
        cfn_id = cfn.create_stack(name, template, parameters=parameters)
        return cfn_id

    def _get_supported_resource(self, requested_type):
        """
        check Resource is supported
        :param requested_type:
        :return: None if not supported
        """
        for service, methods in SUPPORTED_BANDAGE.items():
            if requested_type in methods:
                return service
        return None

    def _get_resource_type(self, resource):
        """

        :param resource: AWS resource type
        :return: postfix of the type
        """
        return resource['Type'].split('::')[-1]

    def patch_bandage(self, region, cfn_stack_id, patch, parameters):
        """
        Patch the target cloudformation
        :param region:
        :param cfn_stack_id:
        :param patch:
        :param parameters:
        :return:
        """
        for key, resource in patch['Resources'].items():
            # check there is a Type attribute
            if not resource.get('Type') or "AWS::" not in resource.get('Type'):
                raise TypeError("%s resource type is invalid" % resource)

            # check before using eval() for safety
            resource_obj = self._get_resource_type(resource)
            service = self._get_supported_resource(resource_obj)
            if service:
                # validate user input
                obj = eval(resource_obj)(**resource)
                obj.validate()
                obj.reference(parameters)

                # connect to AWS
                if isinstance(obj, AWSObject):
                    print service.lower()
                    connection = Connection(service.lower(), SUPPORTED_REGION.get(service, region))
                    print connection
                    if not connection:
                        raise ImportWarning("Cannot connect to aws service %s in region %s"
                                            % service.lower(), SUPPORTED_REGION.get(service, region))

                    # patch
                    cfn_connection = Connection("cloudformation", region)
                    cfn = CloudFormation(connection=cfn_connection.new_connection())
                    obj.depends_on(cfn, cfn_stack_id)
                    obj.patch(connection.new_connection(), cfn_stack_id)
                else:
                    self.logger.debug("Nothing happened")
            else:
                raise ValueError("%s resource is not supported" % resource_obj)
