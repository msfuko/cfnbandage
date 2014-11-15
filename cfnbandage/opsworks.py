import traceback
from . import AWSObject
from . import validator
from lib.opsworks import Opsworks


class OpsworksObject(AWSObject):

    depends = {
        'StackId': None,
        'LayerId': None
    }


class LoadBasedAutoScalingConfigurations(OpsworksObject):

    type = "AWS::OpsWorks::LoadBasedAutoScalingConfigurations"

    props = {
        'DownScaling': (dict, True),
        'Enable': (validator.boolean, False),
        'LayerId': (validator.reference, True),
        'UpScaling': (dict, True)
    }

    def depends_on(self, cfn, cfn_stack_id):
        try:
            self.depends['LayerId'] = cfn.describe_stack_resource(cfn_stack_id,
                                                                  self.Properties['LayerId']).resource_id
        except Exception:
            self.logger.error("Error to parse depends on parameters")
            print traceback.format_exc()

    def patch(self, conn):
        opsworks = Opsworks(connection=conn)
        opsworks.set_load_based_auto_scaling(self.depends['LayerId'], self.Properties['Enable'],
                                             up_scaling=self.Properties['UpScaling'],
                                             down_scaling=self.Properties['DownScaling'])


class Instance(OpsworksObject):

    type = "AWS::OpsWorks::Instance"

    props = {
        "StackId": (validator.reference, True),
        "LayerIds": (validator.reference_list, True),
        "InstanceType": (validator.reference, True),
        "SshKeyName": (validator.reference, True),
        "AutoScalingType": (basestring, False)
    }

    def depends_on(self, cfn, cfn_stack_id):
        try:
            self.depends['StackId'] = cfn.describe_stack_resource(cfn_stack_id, self.Properties['StackId']).resource_id
            self.depends['LayerId'] = cfn.describe_stack_resource(cfn_stack_id,
                                                                  self.Properties['LayerIds'][0]).resource_id
        except Exception:
            self.logger.error("Error to parse depends on parameters")
            print traceback.format_exc()

    def patch(self, conn):
        opsworks = Opsworks(connection=conn)
        opsworks.create_load_instance(self.depends['StackId'], [self.depends['LayerId']],
                                      self.Properties['InstanceType'])


class DataSource(OpsworksObject):

    type = "AWS::OpsWorks::DataSource"

    props = {
        "Arn": (basestring, True),
        "DatabaseName": (basestring, True),
        "Type": (basestring, True)
    }

    def depends_on(self, cfn, cfn_stack_id):
        try:
            self.depends['AppId'] = cfn.describe_stack_resource(cfn_stack_id,
                                                                self.Properties['AppId']).resource_id
        except Exception:
            self.logger.error("Error to parse depends on parameters")
            print traceback.format_exc()

    def patch(self, conn):
        opsworks = Opsworks(connection=conn)
        opsworks.update_app(self.depends['AppId'], self.Properties['DataSources'])

