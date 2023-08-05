# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class MfaDuo(pulumi.CustomResource):
    api_hostname: pulumi.Output[str]
    integration_key: pulumi.Output[str]
    mount_accessor: pulumi.Output[str]
    name: pulumi.Output[str]
    push_info: pulumi.Output[str]
    secret_key: pulumi.Output[str]
    username_format: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, api_hostname=None, integration_key=None, mount_accessor=None, name=None, push_info=None, secret_key=None, username_format=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to manage [Duo MFA](https://www.vaultproject.io/docs/enterprise/mfa/mfa-duo.html).
        
        **Note** this feature is available only with Vault Enterprise.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/mfa_duo.html.markdown.
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

            if api_hostname is None:
                raise TypeError("Missing required property 'api_hostname'")
            __props__['api_hostname'] = api_hostname
            if integration_key is None:
                raise TypeError("Missing required property 'integration_key'")
            __props__['integration_key'] = integration_key
            if mount_accessor is None:
                raise TypeError("Missing required property 'mount_accessor'")
            __props__['mount_accessor'] = mount_accessor
            __props__['name'] = name
            __props__['push_info'] = push_info
            if secret_key is None:
                raise TypeError("Missing required property 'secret_key'")
            __props__['secret_key'] = secret_key
            __props__['username_format'] = username_format
        super(MfaDuo, __self__).__init__(
            'vault:index/mfaDuo:MfaDuo',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_hostname=None, integration_key=None, mount_accessor=None, name=None, push_info=None, secret_key=None, username_format=None):
        """
        Get an existing MfaDuo resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/mfa_duo.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["api_hostname"] = api_hostname
        __props__["integration_key"] = integration_key
        __props__["mount_accessor"] = mount_accessor
        __props__["name"] = name
        __props__["push_info"] = push_info
        __props__["secret_key"] = secret_key
        __props__["username_format"] = username_format
        return MfaDuo(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

