# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Account(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN for this account.
    """
    email: pulumi.Output[str]
    """
    The email address of the owner to assign to the new member account. This email address must not already be associated with another AWS account.
    """
    iam_user_access_to_billing: pulumi.Output[str]
    """
    If set to `ALLOW`, the new account enables IAM users to access account billing information if they have the required permissions. If set to `DENY`, then only the root user of the new account can access account billing information.
    """
    joined_method: pulumi.Output[str]
    joined_timestamp: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    A friendly name for the member account.
    """
    parent_id: pulumi.Output[str]
    """
    Parent Organizational Unit ID or Root ID for the account. Defaults to the Organization default Root ID. A configuration must be present for this argument to perform drift detection.
    """
    role_name: pulumi.Output[str]
    """
    The name of an IAM role that Organizations automatically preconfigures in the new member account. This role trusts the master account, allowing users in the master account to assume the role, as permitted by the master account administrator. The role has administrator permissions in the new member account. The Organizations API provides no method for reading this information after account creation, so this provider cannot perform drift detection on its value and will always show a difference for a configured value after import unless [`ignore_changes`](https://www.terraform.io/docs/configuration/resources.html#ignore_changes) is used.
    """
    status: pulumi.Output[str]
    tags: pulumi.Output[dict]
    """
    Key-value mapping of resource tags.
    """
    def __init__(__self__, resource_name, opts=None, email=None, iam_user_access_to_billing=None, name=None, parent_id=None, role_name=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to create a member account in the current organization.
        
        > **Note:** Account management must be done from the organization's master account.
        
        !> **WARNING:** Deleting this resource will only remove an AWS account from an organization. This provider will not close the account. The member account must be prepared to be a standalone account beforehand. See the [AWS Organizations documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html) for more information.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email: The email address of the owner to assign to the new member account. This email address must not already be associated with another AWS account.
        :param pulumi.Input[str] iam_user_access_to_billing: If set to `ALLOW`, the new account enables IAM users to access account billing information if they have the required permissions. If set to `DENY`, then only the root user of the new account can access account billing information.
        :param pulumi.Input[str] name: A friendly name for the member account.
        :param pulumi.Input[str] parent_id: Parent Organizational Unit ID or Root ID for the account. Defaults to the Organization default Root ID. A configuration must be present for this argument to perform drift detection.
        :param pulumi.Input[str] role_name: The name of an IAM role that Organizations automatically preconfigures in the new member account. This role trusts the master account, allowing users in the master account to assume the role, as permitted by the master account administrator. The role has administrator permissions in the new member account. The Organizations API provides no method for reading this information after account creation, so this provider cannot perform drift detection on its value and will always show a difference for a configured value after import unless [`ignore_changes`](https://www.terraform.io/docs/configuration/resources.html#ignore_changes) is used.
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/organizations_account.html.markdown.
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

            if email is None:
                raise TypeError("Missing required property 'email'")
            __props__['email'] = email
            __props__['iam_user_access_to_billing'] = iam_user_access_to_billing
            __props__['name'] = name
            __props__['parent_id'] = parent_id
            __props__['role_name'] = role_name
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['joined_method'] = None
            __props__['joined_timestamp'] = None
            __props__['status'] = None
        super(Account, __self__).__init__(
            'aws:organizations/account:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, email=None, iam_user_access_to_billing=None, joined_method=None, joined_timestamp=None, name=None, parent_id=None, role_name=None, status=None, tags=None):
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN for this account.
        :param pulumi.Input[str] email: The email address of the owner to assign to the new member account. This email address must not already be associated with another AWS account.
        :param pulumi.Input[str] iam_user_access_to_billing: If set to `ALLOW`, the new account enables IAM users to access account billing information if they have the required permissions. If set to `DENY`, then only the root user of the new account can access account billing information.
        :param pulumi.Input[str] name: A friendly name for the member account.
        :param pulumi.Input[str] parent_id: Parent Organizational Unit ID or Root ID for the account. Defaults to the Organization default Root ID. A configuration must be present for this argument to perform drift detection.
        :param pulumi.Input[str] role_name: The name of an IAM role that Organizations automatically preconfigures in the new member account. This role trusts the master account, allowing users in the master account to assume the role, as permitted by the master account administrator. The role has administrator permissions in the new member account. The Organizations API provides no method for reading this information after account creation, so this provider cannot perform drift detection on its value and will always show a difference for a configured value after import unless [`ignore_changes`](https://www.terraform.io/docs/configuration/resources.html#ignore_changes) is used.
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/organizations_account.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["arn"] = arn
        __props__["email"] = email
        __props__["iam_user_access_to_billing"] = iam_user_access_to_billing
        __props__["joined_method"] = joined_method
        __props__["joined_timestamp"] = joined_timestamp
        __props__["name"] = name
        __props__["parent_id"] = parent_id
        __props__["role_name"] = role_name
        __props__["status"] = status
        __props__["tags"] = tags
        return Account(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

