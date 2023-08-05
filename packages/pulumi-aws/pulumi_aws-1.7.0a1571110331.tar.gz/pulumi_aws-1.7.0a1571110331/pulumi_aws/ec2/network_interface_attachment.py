# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class NetworkInterfaceAttachment(pulumi.CustomResource):
    attachment_id: pulumi.Output[str]
    """
    The ENI Attachment ID.
    """
    device_index: pulumi.Output[float]
    """
    Network interface index (int).
    """
    instance_id: pulumi.Output[str]
    """
    Instance ID to attach.
    """
    network_interface_id: pulumi.Output[str]
    """
    ENI ID to attach.
    """
    status: pulumi.Output[str]
    """
    The status of the Network Interface Attachment.
    """
    def __init__(__self__, resource_name, opts=None, device_index=None, instance_id=None, network_interface_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Attach an Elastic network interface (ENI) resource with EC2 instance.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/network_interface_attachment.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if device_index is None:
                raise TypeError("Missing required property 'device_index'")
            __props__['device_index'] = device_index
            if instance_id is None:
                raise TypeError("Missing required property 'instance_id'")
            __props__['instance_id'] = instance_id
            if network_interface_id is None:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__['network_interface_id'] = network_interface_id
            __props__['attachment_id'] = None
            __props__['status'] = None
        super(NetworkInterfaceAttachment, __self__).__init__(
            'aws:ec2/networkInterfaceAttachment:NetworkInterfaceAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, attachment_id=None, device_index=None, instance_id=None, network_interface_id=None, status=None):
        """
        Get an existing NetworkInterfaceAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attachment_id: The ENI Attachment ID.
        :param pulumi.Input[float] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.
        :param pulumi.Input[str] status: The status of the Network Interface Attachment.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/network_interface_attachment.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["attachment_id"] = attachment_id
        __props__["device_index"] = device_index
        __props__["instance_id"] = instance_id
        __props__["network_interface_id"] = network_interface_id
        __props__["status"] = status
        return NetworkInterfaceAttachment(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

