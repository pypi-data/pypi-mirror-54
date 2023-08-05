# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GeoMatchSet(pulumi.CustomResource):
    geo_match_constraints: pulumi.Output[list]
    """
    The GeoMatchConstraint objects which contain the country that you want AWS WAF to search for.
    
      * `type` (`str`) - The type of geographical area you want AWS WAF to search for. Currently Country is the only valid value.
      * `value` (`str`) - The country that you want AWS WAF to search for.
        This is the two-letter country code, e.g. `US`, `CA`, `RU`, `CN`, etc.
        See [docs](https://docs.aws.amazon.com/waf/latest/APIReference/API_GeoMatchConstraint.html) for all supported values.
    """
    name: pulumi.Output[str]
    """
    The name or description of the GeoMatchSet.
    """
    def __init__(__self__, resource_name, opts=None, geo_match_constraints=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a WAF Geo Match Set Resource
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] geo_match_constraints: The GeoMatchConstraint objects which contain the country that you want AWS WAF to search for.
        :param pulumi.Input[str] name: The name or description of the GeoMatchSet.
        
        The **geo_match_constraints** object supports the following:
        
          * `type` (`pulumi.Input[str]`) - The type of geographical area you want AWS WAF to search for. Currently Country is the only valid value.
          * `value` (`pulumi.Input[str]`) - The country that you want AWS WAF to search for.
            This is the two-letter country code, e.g. `US`, `CA`, `RU`, `CN`, etc.
            See [docs](https://docs.aws.amazon.com/waf/latest/APIReference/API_GeoMatchConstraint.html) for all supported values.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/waf_geo_match_set.html.markdown.
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

            __props__['geo_match_constraints'] = geo_match_constraints
            __props__['name'] = name
        super(GeoMatchSet, __self__).__init__(
            'aws:waf/geoMatchSet:GeoMatchSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, geo_match_constraints=None, name=None):
        """
        Get an existing GeoMatchSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] geo_match_constraints: The GeoMatchConstraint objects which contain the country that you want AWS WAF to search for.
        :param pulumi.Input[str] name: The name or description of the GeoMatchSet.
        
        The **geo_match_constraints** object supports the following:
        
          * `type` (`pulumi.Input[str]`) - The type of geographical area you want AWS WAF to search for. Currently Country is the only valid value.
          * `value` (`pulumi.Input[str]`) - The country that you want AWS WAF to search for.
            This is the two-letter country code, e.g. `US`, `CA`, `RU`, `CN`, etc.
            See [docs](https://docs.aws.amazon.com/waf/latest/APIReference/API_GeoMatchConstraint.html) for all supported values.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/waf_geo_match_set.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["geo_match_constraints"] = geo_match_constraints
        __props__["name"] = name
        return GeoMatchSet(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

