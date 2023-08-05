# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class SecretBackendSign(pulumi.CustomResource):
    alt_names: pulumi.Output[list]
    """
    List of alternative names
    """
    auto_renew: pulumi.Output[bool]
    """
    If set to `true`, certs will be renewed if the expiration is within `min_seconds_remaining`. Default `false`
    """
    backend: pulumi.Output[str]
    """
    The PKI secret backend the resource belongs to.
    """
    ca_chains: pulumi.Output[list]
    """
    The CA chain
    """
    certificate: pulumi.Output[str]
    """
    The certificate
    """
    common_name: pulumi.Output[str]
    """
    CN of certificate to create
    """
    csr: pulumi.Output[str]
    """
    The CSR
    """
    exclude_cn_from_sans: pulumi.Output[bool]
    """
    Flag to exclude CN from SANs
    """
    expiration: pulumi.Output[float]
    """
    The expiration date of the certificate in unix epoch format
    """
    format: pulumi.Output[str]
    """
    The format of data
    """
    ip_sans: pulumi.Output[list]
    """
    List of alternative IPs
    """
    issuing_ca: pulumi.Output[str]
    """
    The issuing CA
    """
    min_seconds_remaining: pulumi.Output[float]
    """
    Generate a new certificate when the expiration is within this number of seconds, default is 604800 (7 days)
    """
    name: pulumi.Output[str]
    """
    Name of the role to create the certificate against
    """
    other_sans: pulumi.Output[list]
    """
    List of other SANs
    """
    serial: pulumi.Output[str]
    """
    The serial
    """
    ttl: pulumi.Output[str]
    """
    Time to live
    """
    uri_sans: pulumi.Output[list]
    """
    List of alterative URIs
    """
    def __init__(__self__, resource_name, opts=None, alt_names=None, auto_renew=None, backend=None, common_name=None, csr=None, exclude_cn_from_sans=None, format=None, ip_sans=None, min_seconds_remaining=None, name=None, other_sans=None, ttl=None, uri_sans=None, __props__=None, __name__=None, __opts__=None):
        """
        Create a SecretBackendSign resource with the given unique name, props, and options.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] alt_names: List of alternative names
        :param pulumi.Input[bool] auto_renew: If set to `true`, certs will be renewed if the expiration is within `min_seconds_remaining`. Default `false`
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[str] common_name: CN of certificate to create
        :param pulumi.Input[str] csr: The CSR
        :param pulumi.Input[bool] exclude_cn_from_sans: Flag to exclude CN from SANs
        :param pulumi.Input[str] format: The format of data
        :param pulumi.Input[list] ip_sans: List of alternative IPs
        :param pulumi.Input[float] min_seconds_remaining: Generate a new certificate when the expiration is within this number of seconds, default is 604800 (7 days)
        :param pulumi.Input[str] name: Name of the role to create the certificate against
        :param pulumi.Input[list] other_sans: List of other SANs
        :param pulumi.Input[str] ttl: Time to live
        :param pulumi.Input[list] uri_sans: List of alterative URIs

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/pki_secret_backend_sign.html.markdown.
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

            __props__['alt_names'] = alt_names
            __props__['auto_renew'] = auto_renew
            if backend is None:
                raise TypeError("Missing required property 'backend'")
            __props__['backend'] = backend
            if common_name is None:
                raise TypeError("Missing required property 'common_name'")
            __props__['common_name'] = common_name
            if csr is None:
                raise TypeError("Missing required property 'csr'")
            __props__['csr'] = csr
            __props__['exclude_cn_from_sans'] = exclude_cn_from_sans
            __props__['format'] = format
            __props__['ip_sans'] = ip_sans
            __props__['min_seconds_remaining'] = min_seconds_remaining
            __props__['name'] = name
            __props__['other_sans'] = other_sans
            __props__['ttl'] = ttl
            __props__['uri_sans'] = uri_sans
            __props__['ca_chains'] = None
            __props__['certificate'] = None
            __props__['expiration'] = None
            __props__['issuing_ca'] = None
            __props__['serial'] = None
        super(SecretBackendSign, __self__).__init__(
            'vault:pkiSecret/secretBackendSign:SecretBackendSign',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, alt_names=None, auto_renew=None, backend=None, ca_chains=None, certificate=None, common_name=None, csr=None, exclude_cn_from_sans=None, expiration=None, format=None, ip_sans=None, issuing_ca=None, min_seconds_remaining=None, name=None, other_sans=None, serial=None, ttl=None, uri_sans=None):
        """
        Get an existing SecretBackendSign resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] alt_names: List of alternative names
        :param pulumi.Input[bool] auto_renew: If set to `true`, certs will be renewed if the expiration is within `min_seconds_remaining`. Default `false`
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[list] ca_chains: The CA chain
        :param pulumi.Input[str] certificate: The certificate
        :param pulumi.Input[str] common_name: CN of certificate to create
        :param pulumi.Input[str] csr: The CSR
        :param pulumi.Input[bool] exclude_cn_from_sans: Flag to exclude CN from SANs
        :param pulumi.Input[float] expiration: The expiration date of the certificate in unix epoch format
        :param pulumi.Input[str] format: The format of data
        :param pulumi.Input[list] ip_sans: List of alternative IPs
        :param pulumi.Input[str] issuing_ca: The issuing CA
        :param pulumi.Input[float] min_seconds_remaining: Generate a new certificate when the expiration is within this number of seconds, default is 604800 (7 days)
        :param pulumi.Input[str] name: Name of the role to create the certificate against
        :param pulumi.Input[list] other_sans: List of other SANs
        :param pulumi.Input[str] serial: The serial
        :param pulumi.Input[str] ttl: Time to live
        :param pulumi.Input[list] uri_sans: List of alterative URIs

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/pki_secret_backend_sign.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["alt_names"] = alt_names
        __props__["auto_renew"] = auto_renew
        __props__["backend"] = backend
        __props__["ca_chains"] = ca_chains
        __props__["certificate"] = certificate
        __props__["common_name"] = common_name
        __props__["csr"] = csr
        __props__["exclude_cn_from_sans"] = exclude_cn_from_sans
        __props__["expiration"] = expiration
        __props__["format"] = format
        __props__["ip_sans"] = ip_sans
        __props__["issuing_ca"] = issuing_ca
        __props__["min_seconds_remaining"] = min_seconds_remaining
        __props__["name"] = name
        __props__["other_sans"] = other_sans
        __props__["serial"] = serial
        __props__["ttl"] = ttl
        __props__["uri_sans"] = uri_sans
        return SecretBackendSign(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

