# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class LoadBalancer(pulumi.CustomResource):
    access_logs: pulumi.Output[dict]
    """
    An Access Logs block. Access Logs documented below.
    
      * `bucket` (`str`) - The S3 bucket name to store the logs in.
      * `enabled` (`bool`) - Boolean to enable / disable `access_logs`. Defaults to `false`, even when `bucket` is specified.
      * `prefix` (`str`) - The S3 bucket prefix. Logs are stored in the root if not configured.
    """
    arn: pulumi.Output[str]
    """
    The ARN of the load balancer (matches `id`).
    """
    arn_suffix: pulumi.Output[str]
    """
    The ARN suffix for use with CloudWatch Metrics.
    """
    dns_name: pulumi.Output[str]
    """
    The DNS name of the load balancer.
    """
    enable_cross_zone_load_balancing: pulumi.Output[bool]
    """
    If true, cross-zone load balancing of the load balancer will be enabled.
    This is a `network` load balancer feature. Defaults to `false`.
    """
    enable_deletion_protection: pulumi.Output[bool]
    """
    If true, deletion of the load balancer will be disabled via
    the AWS API. This will prevent this provider from deleting the load balancer. Defaults to `false`.
    """
    enable_http2: pulumi.Output[bool]
    """
    Indicates whether HTTP/2 is enabled in `application` load balancers. Defaults to `true`.
    """
    idle_timeout: pulumi.Output[float]
    """
    The time in seconds that the connection is allowed to be idle. Only valid for Load Balancers of type `application`. Default: 60.
    """
    internal: pulumi.Output[bool]
    """
    If true, the LB will be internal.
    """
    ip_address_type: pulumi.Output[str]
    """
    The type of IP addresses used by the subnets for your load balancer. The possible values are `ipv4` and `dualstack`
    """
    load_balancer_type: pulumi.Output[str]
    """
    The type of load balancer to create. Possible values are `application` or `network`. The default value is `application`.
    """
    name: pulumi.Output[str]
    """
    The name of the LB. This name must be unique within your AWS account, can have a maximum of 32 characters,
    must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. If not specified,
    this provider will autogenerate a name beginning with `tf-lb`.
    """
    name_prefix: pulumi.Output[str]
    """
    Creates a unique name beginning with the specified prefix. Conflicts with `name`.
    """
    security_groups: pulumi.Output[list]
    """
    A list of security group IDs to assign to the LB. Only valid for Load Balancers of type `application`.
    """
    subnet_mappings: pulumi.Output[list]
    """
    A subnet mapping block as documented below.
    
      * `allocation_id` (`str`) - The allocation ID of the Elastic IP address.
      * `subnet_id` (`str`) - The id of the subnet of which to attach to the load balancer. You can specify only one subnet per Availability Zone.
    """
    subnets: pulumi.Output[list]
    """
    A list of subnet IDs to attach to the LB. Subnets
    cannot be updated for Load Balancers of type `network`. Changing this value
    for load balancers of type `network` will force a recreation of the resource.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    vpc_id: pulumi.Output[str]
    zone_id: pulumi.Output[str]
    """
    The canonical hosted zone ID of the load balancer (to be used in a Route 53 Alias record).
    """
    def __init__(__self__, resource_name, opts=None, access_logs=None, enable_cross_zone_load_balancing=None, enable_deletion_protection=None, enable_http2=None, idle_timeout=None, internal=None, ip_address_type=None, load_balancer_type=None, name=None, name_prefix=None, security_groups=None, subnet_mappings=None, subnets=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Load Balancer resource.
        
        > **Note:** `alb.LoadBalancer` is known as `lb.LoadBalancer`. The functionality is identical.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] access_logs: An Access Logs block. Access Logs documented below.
        :param pulumi.Input[bool] enable_cross_zone_load_balancing: If true, cross-zone load balancing of the load balancer will be enabled.
               This is a `network` load balancer feature. Defaults to `false`.
        :param pulumi.Input[bool] enable_deletion_protection: If true, deletion of the load balancer will be disabled via
               the AWS API. This will prevent this provider from deleting the load balancer. Defaults to `false`.
        :param pulumi.Input[bool] enable_http2: Indicates whether HTTP/2 is enabled in `application` load balancers. Defaults to `true`.
        :param pulumi.Input[float] idle_timeout: The time in seconds that the connection is allowed to be idle. Only valid for Load Balancers of type `application`. Default: 60.
        :param pulumi.Input[bool] internal: If true, the LB will be internal.
        :param pulumi.Input[str] ip_address_type: The type of IP addresses used by the subnets for your load balancer. The possible values are `ipv4` and `dualstack`
        :param pulumi.Input[str] load_balancer_type: The type of load balancer to create. Possible values are `application` or `network`. The default value is `application`.
        :param pulumi.Input[str] name: The name of the LB. This name must be unique within your AWS account, can have a maximum of 32 characters,
               must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. If not specified,
               this provider will autogenerate a name beginning with `tf-lb`.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[list] security_groups: A list of security group IDs to assign to the LB. Only valid for Load Balancers of type `application`.
        :param pulumi.Input[list] subnet_mappings: A subnet mapping block as documented below.
        :param pulumi.Input[list] subnets: A list of subnet IDs to attach to the LB. Subnets
               cannot be updated for Load Balancers of type `network`. Changing this value
               for load balancers of type `network` will force a recreation of the resource.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        
        The **access_logs** object supports the following:
        
          * `bucket` (`pulumi.Input[str]`) - The S3 bucket name to store the logs in.
          * `enabled` (`pulumi.Input[bool]`) - Boolean to enable / disable `access_logs`. Defaults to `false`, even when `bucket` is specified.
          * `prefix` (`pulumi.Input[str]`) - The S3 bucket prefix. Logs are stored in the root if not configured.
        
        The **subnet_mappings** object supports the following:
        
          * `allocation_id` (`pulumi.Input[str]`) - The allocation ID of the Elastic IP address.
          * `subnet_id` (`pulumi.Input[str]`) - The id of the subnet of which to attach to the load balancer. You can specify only one subnet per Availability Zone.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/lb_legacy.html.markdown.
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

            __props__['access_logs'] = access_logs
            __props__['enable_cross_zone_load_balancing'] = enable_cross_zone_load_balancing
            __props__['enable_deletion_protection'] = enable_deletion_protection
            __props__['enable_http2'] = enable_http2
            __props__['idle_timeout'] = idle_timeout
            __props__['internal'] = internal
            __props__['ip_address_type'] = ip_address_type
            __props__['load_balancer_type'] = load_balancer_type
            __props__['name'] = name
            __props__['name_prefix'] = name_prefix
            __props__['security_groups'] = security_groups
            __props__['subnet_mappings'] = subnet_mappings
            __props__['subnets'] = subnets
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['arn_suffix'] = None
            __props__['dns_name'] = None
            __props__['vpc_id'] = None
            __props__['zone_id'] = None
        super(LoadBalancer, __self__).__init__(
            'aws:elasticloadbalancingv2/loadBalancer:LoadBalancer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, access_logs=None, arn=None, arn_suffix=None, dns_name=None, enable_cross_zone_load_balancing=None, enable_deletion_protection=None, enable_http2=None, idle_timeout=None, internal=None, ip_address_type=None, load_balancer_type=None, name=None, name_prefix=None, security_groups=None, subnet_mappings=None, subnets=None, tags=None, vpc_id=None, zone_id=None):
        """
        Get an existing LoadBalancer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] access_logs: An Access Logs block. Access Logs documented below.
        :param pulumi.Input[str] arn: The ARN of the load balancer (matches `id`).
        :param pulumi.Input[str] arn_suffix: The ARN suffix for use with CloudWatch Metrics.
        :param pulumi.Input[str] dns_name: The DNS name of the load balancer.
        :param pulumi.Input[bool] enable_cross_zone_load_balancing: If true, cross-zone load balancing of the load balancer will be enabled.
               This is a `network` load balancer feature. Defaults to `false`.
        :param pulumi.Input[bool] enable_deletion_protection: If true, deletion of the load balancer will be disabled via
               the AWS API. This will prevent this provider from deleting the load balancer. Defaults to `false`.
        :param pulumi.Input[bool] enable_http2: Indicates whether HTTP/2 is enabled in `application` load balancers. Defaults to `true`.
        :param pulumi.Input[float] idle_timeout: The time in seconds that the connection is allowed to be idle. Only valid for Load Balancers of type `application`. Default: 60.
        :param pulumi.Input[bool] internal: If true, the LB will be internal.
        :param pulumi.Input[str] ip_address_type: The type of IP addresses used by the subnets for your load balancer. The possible values are `ipv4` and `dualstack`
        :param pulumi.Input[str] load_balancer_type: The type of load balancer to create. Possible values are `application` or `network`. The default value is `application`.
        :param pulumi.Input[str] name: The name of the LB. This name must be unique within your AWS account, can have a maximum of 32 characters,
               must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. If not specified,
               this provider will autogenerate a name beginning with `tf-lb`.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[list] security_groups: A list of security group IDs to assign to the LB. Only valid for Load Balancers of type `application`.
        :param pulumi.Input[list] subnet_mappings: A subnet mapping block as documented below.
        :param pulumi.Input[list] subnets: A list of subnet IDs to attach to the LB. Subnets
               cannot be updated for Load Balancers of type `network`. Changing this value
               for load balancers of type `network` will force a recreation of the resource.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] zone_id: The canonical hosted zone ID of the load balancer (to be used in a Route 53 Alias record).
        
        The **access_logs** object supports the following:
        
          * `bucket` (`pulumi.Input[str]`) - The S3 bucket name to store the logs in.
          * `enabled` (`pulumi.Input[bool]`) - Boolean to enable / disable `access_logs`. Defaults to `false`, even when `bucket` is specified.
          * `prefix` (`pulumi.Input[str]`) - The S3 bucket prefix. Logs are stored in the root if not configured.
        
        The **subnet_mappings** object supports the following:
        
          * `allocation_id` (`pulumi.Input[str]`) - The allocation ID of the Elastic IP address.
          * `subnet_id` (`pulumi.Input[str]`) - The id of the subnet of which to attach to the load balancer. You can specify only one subnet per Availability Zone.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/lb_legacy.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["access_logs"] = access_logs
        __props__["arn"] = arn
        __props__["arn_suffix"] = arn_suffix
        __props__["dns_name"] = dns_name
        __props__["enable_cross_zone_load_balancing"] = enable_cross_zone_load_balancing
        __props__["enable_deletion_protection"] = enable_deletion_protection
        __props__["enable_http2"] = enable_http2
        __props__["idle_timeout"] = idle_timeout
        __props__["internal"] = internal
        __props__["ip_address_type"] = ip_address_type
        __props__["load_balancer_type"] = load_balancer_type
        __props__["name"] = name
        __props__["name_prefix"] = name_prefix
        __props__["security_groups"] = security_groups
        __props__["subnet_mappings"] = subnet_mappings
        __props__["subnets"] = subnets
        __props__["tags"] = tags
        __props__["vpc_id"] = vpc_id
        __props__["zone_id"] = zone_id
        return LoadBalancer(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

