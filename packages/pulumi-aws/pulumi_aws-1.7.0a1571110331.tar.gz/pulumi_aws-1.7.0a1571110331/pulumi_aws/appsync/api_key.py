# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ApiKey(pulumi.CustomResource):
    api_id: pulumi.Output[str]
    """
    The ID of the associated AppSync API
    """
    description: pulumi.Output[str]
    """
    The API key description. Defaults to "Managed by Pulumi".
    """
    expires: pulumi.Output[str]
    """
    RFC3339 string representation of the expiry date. Rounded down to nearest hour. By default, it is 7 days from the date of creation.
    """
    key: pulumi.Output[str]
    """
    The API key
    """
    def __init__(__self__, resource_name, opts=None, api_id=None, description=None, expires=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AppSync API Key.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: The ID of the associated AppSync API
        :param pulumi.Input[str] description: The API key description. Defaults to "Managed by Pulumi".
        :param pulumi.Input[str] expires: RFC3339 string representation of the expiry date. Rounded down to nearest hour. By default, it is 7 days from the date of creation.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appsync_api_key.html.markdown.
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

            if api_id is None:
                raise TypeError("Missing required property 'api_id'")
            __props__['api_id'] = api_id
            __props__['description'] = description
            __props__['expires'] = expires
            __props__['key'] = None
        super(ApiKey, __self__).__init__(
            'aws:appsync/apiKey:ApiKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_id=None, description=None, expires=None, key=None):
        """
        Get an existing ApiKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: The ID of the associated AppSync API
        :param pulumi.Input[str] description: The API key description. Defaults to "Managed by Pulumi".
        :param pulumi.Input[str] expires: RFC3339 string representation of the expiry date. Rounded down to nearest hour. By default, it is 7 days from the date of creation.
        :param pulumi.Input[str] key: The API key

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appsync_api_key.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["api_id"] = api_id
        __props__["description"] = description
        __props__["expires"] = expires
        __props__["key"] = key
        return ApiKey(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

