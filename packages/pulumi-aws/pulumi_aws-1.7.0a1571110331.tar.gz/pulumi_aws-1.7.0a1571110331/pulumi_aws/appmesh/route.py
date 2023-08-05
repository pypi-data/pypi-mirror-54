# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Route(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the route.
    """
    created_date: pulumi.Output[str]
    """
    The creation date of the route.
    """
    last_updated_date: pulumi.Output[str]
    """
    The last update date of the route.
    """
    mesh_name: pulumi.Output[str]
    """
    The name of the service mesh in which to create the route.
    """
    name: pulumi.Output[str]
    """
    The name to use for the route.
    """
    spec: pulumi.Output[dict]
    """
    The route specification to apply.
    
      * `httpRoute` (`dict`) - The HTTP routing information for the route.
    
        * `action` (`dict`) - The action to take if a match is determined.
    
          * `weightedTargets` (`list`) - The targets that traffic is routed to when a request matches the route.
            You can specify one or more targets and their relative weights with which to distribute traffic.
    
            * `virtualNode` (`str`) - The virtual node to associate with the weighted target.
            * `weight` (`float`) - The relative weight of the weighted target. An integer between 0 and 100.
    
        * `match` (`dict`) - The criteria for determining an HTTP request match.
    
          * `prefix` (`str`) - Specifies the path with which to match requests.
            This parameter must always start with /, which by itself matches all requests to the virtual router service name.
    
      * `tcpRoute` (`dict`) - The TCP routing information for the route.
    
        * `action` (`dict`) - The action to take if a match is determined.
    
          * `weightedTargets` (`list`) - The targets that traffic is routed to when a request matches the route.
            You can specify one or more targets and their relative weights with which to distribute traffic.
    
            * `virtualNode` (`str`) - The virtual node to associate with the weighted target.
            * `weight` (`float`) - The relative weight of the weighted target. An integer between 0 and 100.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    virtual_router_name: pulumi.Output[str]
    """
    The name of the virtual router in which to create the route.
    """
    def __init__(__self__, resource_name, opts=None, mesh_name=None, name=None, spec=None, tags=None, virtual_router_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AWS App Mesh route resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] mesh_name: The name of the service mesh in which to create the route.
        :param pulumi.Input[str] name: The name to use for the route.
        :param pulumi.Input[dict] spec: The route specification to apply.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] virtual_router_name: The name of the virtual router in which to create the route.
        
        The **spec** object supports the following:
        
          * `httpRoute` (`pulumi.Input[dict]`) - The HTTP routing information for the route.
        
            * `action` (`pulumi.Input[dict]`) - The action to take if a match is determined.
        
              * `weightedTargets` (`pulumi.Input[list]`) - The targets that traffic is routed to when a request matches the route.
                You can specify one or more targets and their relative weights with which to distribute traffic.
        
                * `virtualNode` (`pulumi.Input[str]`) - The virtual node to associate with the weighted target.
                * `weight` (`pulumi.Input[float]`) - The relative weight of the weighted target. An integer between 0 and 100.
        
            * `match` (`pulumi.Input[dict]`) - The criteria for determining an HTTP request match.
        
              * `prefix` (`pulumi.Input[str]`) - Specifies the path with which to match requests.
                This parameter must always start with /, which by itself matches all requests to the virtual router service name.
        
          * `tcpRoute` (`pulumi.Input[dict]`) - The TCP routing information for the route.
        
            * `action` (`pulumi.Input[dict]`) - The action to take if a match is determined.
        
              * `weightedTargets` (`pulumi.Input[list]`) - The targets that traffic is routed to when a request matches the route.
                You can specify one or more targets and their relative weights with which to distribute traffic.
        
                * `virtualNode` (`pulumi.Input[str]`) - The virtual node to associate with the weighted target.
                * `weight` (`pulumi.Input[float]`) - The relative weight of the weighted target. An integer between 0 and 100.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appmesh_route.html.markdown.
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

            if mesh_name is None:
                raise TypeError("Missing required property 'mesh_name'")
            __props__['mesh_name'] = mesh_name
            __props__['name'] = name
            if spec is None:
                raise TypeError("Missing required property 'spec'")
            __props__['spec'] = spec
            __props__['tags'] = tags
            if virtual_router_name is None:
                raise TypeError("Missing required property 'virtual_router_name'")
            __props__['virtual_router_name'] = virtual_router_name
            __props__['arn'] = None
            __props__['created_date'] = None
            __props__['last_updated_date'] = None
        super(Route, __self__).__init__(
            'aws:appmesh/route:Route',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, created_date=None, last_updated_date=None, mesh_name=None, name=None, spec=None, tags=None, virtual_router_name=None):
        """
        Get an existing Route resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the route.
        :param pulumi.Input[str] created_date: The creation date of the route.
        :param pulumi.Input[str] last_updated_date: The last update date of the route.
        :param pulumi.Input[str] mesh_name: The name of the service mesh in which to create the route.
        :param pulumi.Input[str] name: The name to use for the route.
        :param pulumi.Input[dict] spec: The route specification to apply.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] virtual_router_name: The name of the virtual router in which to create the route.
        
        The **spec** object supports the following:
        
          * `httpRoute` (`pulumi.Input[dict]`) - The HTTP routing information for the route.
        
            * `action` (`pulumi.Input[dict]`) - The action to take if a match is determined.
        
              * `weightedTargets` (`pulumi.Input[list]`) - The targets that traffic is routed to when a request matches the route.
                You can specify one or more targets and their relative weights with which to distribute traffic.
        
                * `virtualNode` (`pulumi.Input[str]`) - The virtual node to associate with the weighted target.
                * `weight` (`pulumi.Input[float]`) - The relative weight of the weighted target. An integer between 0 and 100.
        
            * `match` (`pulumi.Input[dict]`) - The criteria for determining an HTTP request match.
        
              * `prefix` (`pulumi.Input[str]`) - Specifies the path with which to match requests.
                This parameter must always start with /, which by itself matches all requests to the virtual router service name.
        
          * `tcpRoute` (`pulumi.Input[dict]`) - The TCP routing information for the route.
        
            * `action` (`pulumi.Input[dict]`) - The action to take if a match is determined.
        
              * `weightedTargets` (`pulumi.Input[list]`) - The targets that traffic is routed to when a request matches the route.
                You can specify one or more targets and their relative weights with which to distribute traffic.
        
                * `virtualNode` (`pulumi.Input[str]`) - The virtual node to associate with the weighted target.
                * `weight` (`pulumi.Input[float]`) - The relative weight of the weighted target. An integer between 0 and 100.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/appmesh_route.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["created_date"] = created_date
        __props__["last_updated_date"] = last_updated_date
        __props__["mesh_name"] = mesh_name
        __props__["name"] = name
        __props__["spec"] = spec
        __props__["tags"] = tags
        __props__["virtual_router_name"] = virtual_router_name
        return Route(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

