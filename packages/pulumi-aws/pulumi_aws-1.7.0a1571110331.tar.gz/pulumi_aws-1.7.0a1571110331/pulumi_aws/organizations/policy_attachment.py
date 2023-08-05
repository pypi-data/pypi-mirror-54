# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class PolicyAttachment(pulumi.CustomResource):
    policy_id: pulumi.Output[str]
    """
    The unique identifier (ID) of the policy that you want to attach to the target.
    """
    target_id: pulumi.Output[str]
    """
    The unique identifier (ID) of the root, organizational unit, or account number that you want to attach the policy to.
    """
    def __init__(__self__, resource_name, opts=None, policy_id=None, target_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to attach an AWS Organizations policy to an organization account, root, or unit.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_id: The unique identifier (ID) of the policy that you want to attach to the target.
        :param pulumi.Input[str] target_id: The unique identifier (ID) of the root, organizational unit, or account number that you want to attach the policy to.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/organizations_policy_attachment.html.markdown.
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

            if policy_id is None:
                raise TypeError("Missing required property 'policy_id'")
            __props__['policy_id'] = policy_id
            if target_id is None:
                raise TypeError("Missing required property 'target_id'")
            __props__['target_id'] = target_id
        super(PolicyAttachment, __self__).__init__(
            'aws:organizations/policyAttachment:PolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, policy_id=None, target_id=None):
        """
        Get an existing PolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_id: The unique identifier (ID) of the policy that you want to attach to the target.
        :param pulumi.Input[str] target_id: The unique identifier (ID) of the root, organizational unit, or account number that you want to attach the policy to.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/organizations_policy_attachment.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["policy_id"] = policy_id
        __props__["target_id"] = target_id
        return PolicyAttachment(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

