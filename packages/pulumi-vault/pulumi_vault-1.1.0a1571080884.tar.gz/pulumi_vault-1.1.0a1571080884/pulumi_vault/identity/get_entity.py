# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetEntityResult:
    """
    A collection of values returned by getEntity.
    """
    def __init__(__self__, alias_id=None, alias_mount_accessor=None, alias_name=None, aliases=None, creation_time=None, data_json=None, direct_group_ids=None, disabled=None, entity_id=None, entity_name=None, group_ids=None, inherited_group_ids=None, last_update_time=None, merged_entity_ids=None, metadata=None, namespace_id=None, policies=None, id=None):
        if alias_id and not isinstance(alias_id, str):
            raise TypeError("Expected argument 'alias_id' to be a str")
        __self__.alias_id = alias_id
        if alias_mount_accessor and not isinstance(alias_mount_accessor, str):
            raise TypeError("Expected argument 'alias_mount_accessor' to be a str")
        __self__.alias_mount_accessor = alias_mount_accessor
        if alias_name and not isinstance(alias_name, str):
            raise TypeError("Expected argument 'alias_name' to be a str")
        __self__.alias_name = alias_name
        if aliases and not isinstance(aliases, list):
            raise TypeError("Expected argument 'aliases' to be a list")
        __self__.aliases = aliases
        """
        A list of entity alias. Structure is documented below.
        """
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        __self__.creation_time = creation_time
        """
        Creation time of the Alias
        """
        if data_json and not isinstance(data_json, str):
            raise TypeError("Expected argument 'data_json' to be a str")
        __self__.data_json = data_json
        """
        A string containing the full data payload retrieved from
        Vault, serialized in JSON format.
        """
        if direct_group_ids and not isinstance(direct_group_ids, list):
            raise TypeError("Expected argument 'direct_group_ids' to be a list")
        __self__.direct_group_ids = direct_group_ids
        """
        List of Group IDs of which the entity is directly a member of
        """
        if disabled and not isinstance(disabled, bool):
            raise TypeError("Expected argument 'disabled' to be a bool")
        __self__.disabled = disabled
        """
        Whether the entity is disabled
        """
        if entity_id and not isinstance(entity_id, str):
            raise TypeError("Expected argument 'entity_id' to be a str")
        __self__.entity_id = entity_id
        if entity_name and not isinstance(entity_name, str):
            raise TypeError("Expected argument 'entity_name' to be a str")
        __self__.entity_name = entity_name
        if group_ids and not isinstance(group_ids, list):
            raise TypeError("Expected argument 'group_ids' to be a list")
        __self__.group_ids = group_ids
        """
        List of all Group IDs of which the entity is a member of
        """
        if inherited_group_ids and not isinstance(inherited_group_ids, list):
            raise TypeError("Expected argument 'inherited_group_ids' to be a list")
        __self__.inherited_group_ids = inherited_group_ids
        """
        List of all Group IDs of which the entity is a member of transitively
        """
        if last_update_time and not isinstance(last_update_time, str):
            raise TypeError("Expected argument 'last_update_time' to be a str")
        __self__.last_update_time = last_update_time
        """
        Last update time of the alias
        """
        if merged_entity_ids and not isinstance(merged_entity_ids, list):
            raise TypeError("Expected argument 'merged_entity_ids' to be a list")
        __self__.merged_entity_ids = merged_entity_ids
        """
        Other entity IDs which is merged with this entity
        """
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        __self__.metadata = metadata
        """
        Arbitrary metadata
        """
        if namespace_id and not isinstance(namespace_id, str):
            raise TypeError("Expected argument 'namespace_id' to be a str")
        __self__.namespace_id = namespace_id
        """
        Namespace of which the entity is part of
        """
        if policies and not isinstance(policies, list):
            raise TypeError("Expected argument 'policies' to be a list")
        __self__.policies = policies
        """
        List of policies attached to the entity
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetEntityResult(GetEntityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEntityResult(
            alias_id=self.alias_id,
            alias_mount_accessor=self.alias_mount_accessor,
            alias_name=self.alias_name,
            aliases=self.aliases,
            creation_time=self.creation_time,
            data_json=self.data_json,
            direct_group_ids=self.direct_group_ids,
            disabled=self.disabled,
            entity_id=self.entity_id,
            entity_name=self.entity_name,
            group_ids=self.group_ids,
            inherited_group_ids=self.inherited_group_ids,
            last_update_time=self.last_update_time,
            merged_entity_ids=self.merged_entity_ids,
            metadata=self.metadata,
            namespace_id=self.namespace_id,
            policies=self.policies,
            id=self.id)

def get_entity(alias_id=None,alias_mount_accessor=None,alias_name=None,entity_id=None,entity_name=None,opts=None):
    """
    Use this data source to access information about an existing resource.
    
    :param str alias_id: ID of the alias.
    :param str alias_mount_accessor: Accessor of the mount to which the alias belongs to.
           This should be supplied in conjunction with `alias_name`.
    :param str alias_name: Name of the alias. This should be supplied in conjunction with
           `alias_mount_accessor`.
    :param str entity_id: ID of the entity.
    :param str entity_name: Name of the entity.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/d/identity_entity.html.markdown.
    """
    __args__ = dict()

    __args__['aliasId'] = alias_id
    __args__['aliasMountAccessor'] = alias_mount_accessor
    __args__['aliasName'] = alias_name
    __args__['entityId'] = entity_id
    __args__['entityName'] = entity_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('vault:identity/getEntity:getEntity', __args__, opts=opts).value

    return AwaitableGetEntityResult(
        alias_id=__ret__.get('aliasId'),
        alias_mount_accessor=__ret__.get('aliasMountAccessor'),
        alias_name=__ret__.get('aliasName'),
        aliases=__ret__.get('aliases'),
        creation_time=__ret__.get('creationTime'),
        data_json=__ret__.get('dataJson'),
        direct_group_ids=__ret__.get('directGroupIds'),
        disabled=__ret__.get('disabled'),
        entity_id=__ret__.get('entityId'),
        entity_name=__ret__.get('entityName'),
        group_ids=__ret__.get('groupIds'),
        inherited_group_ids=__ret__.get('inheritedGroupIds'),
        last_update_time=__ret__.get('lastUpdateTime'),
        merged_entity_ids=__ret__.get('mergedEntityIds'),
        metadata=__ret__.get('metadata'),
        namespace_id=__ret__.get('namespaceId'),
        policies=__ret__.get('policies'),
        id=__ret__.get('id'))
