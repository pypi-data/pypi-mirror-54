# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Portfolio(pulumi.CustomResource):
    arn: pulumi.Output[str]
    created_time: pulumi.Output[str]
    description: pulumi.Output[str]
    """
    Description of the portfolio
    """
    name: pulumi.Output[str]
    """
    The name of the portfolio.
    """
    provider_name: pulumi.Output[str]
    """
    Name of the person or organization who owns the portfolio.
    """
    tags: pulumi.Output[dict]
    """
    Tags to apply to the connection.
    """
    def __init__(__self__, resource_name, opts=None, description=None, name=None, provider_name=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to create a Service Catalog Portfolio.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the portfolio
        :param pulumi.Input[str] name: The name of the portfolio.
        :param pulumi.Input[str] provider_name: Name of the person or organization who owns the portfolio.
        :param pulumi.Input[dict] tags: Tags to apply to the connection.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/servicecatalog_portfolio.html.markdown.
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

            __props__['description'] = description
            __props__['name'] = name
            __props__['provider_name'] = provider_name
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['created_time'] = None
        super(Portfolio, __self__).__init__(
            'aws:servicecatalog/portfolio:Portfolio',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, created_time=None, description=None, name=None, provider_name=None, tags=None):
        """
        Get an existing Portfolio resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the portfolio
        :param pulumi.Input[str] name: The name of the portfolio.
        :param pulumi.Input[str] provider_name: Name of the person or organization who owns the portfolio.
        :param pulumi.Input[dict] tags: Tags to apply to the connection.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/servicecatalog_portfolio.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["created_time"] = created_time
        __props__["description"] = description
        __props__["name"] = name
        __props__["provider_name"] = provider_name
        __props__["tags"] = tags
        return Portfolio(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

