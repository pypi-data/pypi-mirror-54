# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

_SNAKE_TO_CAMEL_CASE_TABLE = {
    "access_key": "accessKey",
    "account_id": "accountId",
    "add_group_aliases": "addGroupAliases",
    "allow_any_name": "allowAnyName",
    "allow_bare_domains": "allowBareDomains",
    "allow_gce_inference": "allowGceInference",
    "allow_glob_domains": "allowGlobDomains",
    "allow_host_certificates": "allowHostCertificates",
    "allow_instance_migration": "allowInstanceMigration",
    "allow_ip_sans": "allowIpSans",
    "allow_localhost": "allowLocalhost",
    "allow_plaintext_backup": "allowPlaintextBackup",
    "allow_subdomains": "allowSubdomains",
    "allow_user_certificates": "allowUserCertificates",
    "allow_user_key_ids": "allowUserKeyIds",
    "allowed_client_id": "allowedClientId",
    "allowed_client_ids": "allowedClientIds",
    "allowed_common_names": "allowedCommonNames",
    "allowed_critical_options": "allowedCriticalOptions",
    "allowed_dns_sans": "allowedDnsSans",
    "allowed_domains": "allowedDomains",
    "allowed_email_sans": "allowedEmailSans",
    "allowed_extensions": "allowedExtensions",
    "allowed_names": "allowedNames",
    "allowed_organization_units": "allowedOrganizationUnits",
    "allowed_other_sans": "allowedOtherSans",
    "allowed_policies": "allowedPolicies",
    "allowed_redirect_uris": "allowedRedirectUris",
    "allowed_roles": "allowedRoles",
    "allowed_uri_sans": "allowedUriSans",
    "allowed_users": "allowedUsers",
    "alt_names": "altNames",
    "api_hostname": "apiHostname",
    "application_object_id": "applicationObjectId",
    "auth_type": "authType",
    "auto_renew": "autoRenew",
    "aws_public_cert": "awsPublicCert",
    "azure_roles": "azureRoles",
    "base_url": "baseUrl",
    "basic_constraints_valid_for_non_ca": "basicConstraintsValidForNonCa",
    "bind_secret_id": "bindSecretId",
    "bound_account_ids": "boundAccountIds",
    "bound_ami_ids": "boundAmiIds",
    "bound_audiences": "boundAudiences",
    "bound_cidr_lists": "boundCidrLists",
    "bound_cidrs": "boundCidrs",
    "bound_claims": "boundClaims",
    "bound_ec2_instance_ids": "boundEc2InstanceIds",
    "bound_group_ids": "boundGroupIds",
    "bound_iam_instance_profile_arns": "boundIamInstanceProfileArns",
    "bound_iam_principal_arns": "boundIamPrincipalArns",
    "bound_iam_role_arns": "boundIamRoleArns",
    "bound_instance_groups": "boundInstanceGroups",
    "bound_issuer": "boundIssuer",
    "bound_labels": "boundLabels",
    "bound_locations": "boundLocations",
    "bound_projects": "boundProjects",
    "bound_regions": "boundRegions",
    "bound_resource_groups": "boundResourceGroups",
    "bound_scale_sets": "boundScaleSets",
    "bound_service_account_names": "boundServiceAccountNames",
    "bound_service_account_namespaces": "boundServiceAccountNamespaces",
    "bound_service_accounts": "boundServiceAccounts",
    "bound_service_principal_ids": "boundServicePrincipalIds",
    "bound_subject": "boundSubject",
    "bound_subnet_ids": "boundSubnetIds",
    "bound_subscription_ids": "boundSubscriptionIds",
    "bound_vpc_ids": "boundVpcIds",
    "bound_zones": "boundZones",
    "bypass_okta_mfa": "bypassOktaMfa",
    "ca_cert_dir": "caCertDir",
    "ca_cert_file": "caCertFile",
    "ca_chain": "caChain",
    "ca_chains": "caChains",
    "canonical_id": "canonicalId",
    "cert_name": "certName",
    "cidr_list": "cidrList",
    "cidr_lists": "cidrLists",
    "claim_mappings": "claimMappings",
    "client_auths": "clientAuths",
    "client_email": "clientEmail",
    "client_flag": "clientFlag",
    "client_id": "clientId",
    "client_secret": "clientSecret",
    "client_token": "clientToken",
    "code_signing_flag": "codeSigningFlag",
    "common_name": "commonName",
    "connection_uri": "connectionUri",
    "convergent_encryption": "convergentEncryption",
    "creation_statements": "creationStatements",
    "credential_type": "credentialType",
    "crl_distribution_points": "crlDistributionPoints",
    "data_json": "dataJson",
    "db_name": "dbName",
    "default_critical_options": "defaultCriticalOptions",
    "default_extensions": "defaultExtensions",
    "default_lease_ttl_seconds": "defaultLeaseTtlSeconds",
    "default_role": "defaultRole",
    "default_sts_ttl": "defaultStsTtl",
    "default_ttl": "defaultTtl",
    "default_user": "defaultUser",
    "deletion_allowed": "deletionAllowed",
    "deny_null_bind": "denyNullBind",
    "disable_delete": "disableDelete",
    "disable_periodic_tidy": "disablePeriodicTidy",
    "disable_read": "disableRead",
    "disallow_reauthentication": "disallowReauthentication",
    "disallowed_policies": "disallowedPolicies",
    "display_name": "displayName",
    "ec2_endpoint": "ec2Endpoint",
    "email_protection_flag": "emailProtectionFlag",
    "enforce_hostnames": "enforceHostnames",
    "enforcement_level": "enforcementLevel",
    "exclude_cn_from_sans": "excludeCnFromSans",
    "explicit_max_ttl": "explicitMaxTtl",
    "ext_key_usages": "extKeyUsages",
    "external_policies": "externalPolicies",
    "generate_lease": "generateLease",
    "generate_signing_key": "generateSigningKey",
    "group_id": "groupId",
    "group_name": "groupName",
    "groups_claim": "groupsClaim",
    "groups_claim_delimiter_pattern": "groupsClaimDelimiterPattern",
    "iam_endpoint": "iamEndpoint",
    "iam_http_request_method": "iamHttpRequestMethod",
    "iam_request_body": "iamRequestBody",
    "iam_request_headers": "iamRequestHeaders",
    "iam_request_url": "iamRequestUrl",
    "iam_server_id_header_value": "iamServerIdHeaderValue",
    "ignore_absent_fields": "ignoreAbsentFields",
    "inferred_aws_region": "inferredAwsRegion",
    "inferred_entity_type": "inferredEntityType",
    "insecure_tls": "insecureTls",
    "instance_id": "instanceId",
    "integration_key": "integrationKey",
    "ip_sans": "ipSans",
    "issuing_ca": "issuingCa",
    "issuing_certificates": "issuingCertificates",
    "jwks_ca_pem": "jwksCaPem",
    "jwks_url": "jwksUrl",
    "jwt_supported_algs": "jwtSupportedAlgs",
    "jwt_validation_pubkeys": "jwtValidationPubkeys",
    "key_bits": "keyBits",
    "key_id_format": "keyIdFormat",
    "key_name": "keyName",
    "key_type": "keyType",
    "key_usages": "keyUsages",
    "kubernetes_ca_cert": "kubernetesCaCert",
    "kubernetes_host": "kubernetesHost",
    "latest_version": "latestVersion",
    "lease_duration": "leaseDuration",
    "lease_start_time": "leaseStartTime",
    "lease_started": "leaseStarted",
    "listing_visibility": "listingVisibility",
    "max_jwt_exp": "maxJwtExp",
    "max_lease_ttl_seconds": "maxLeaseTtlSeconds",
    "max_path_length": "maxPathLength",
    "max_retries": "maxRetries",
    "max_sts_ttl": "maxStsTtl",
    "max_ttl": "maxTtl",
    "member_entity_ids": "memberEntityIds",
    "member_group_ids": "memberGroupIds",
    "min_available_version": "minAvailableVersion",
    "min_decryption_version": "minDecryptionVersion",
    "min_encryption_version": "minEncryptionVersion",
    "min_seconds_remaining": "minSecondsRemaining",
    "mount_accessor": "mountAccessor",
    "mysql_aurora": "mysqlAurora",
    "mysql_legacy": "mysqlLegacy",
    "mysql_rds": "mysqlRds",
    "no_default_policy": "noDefaultPolicy",
    "no_parent": "noParent",
    "no_store": "noStore",
    "num_uses": "numUses",
    "ocsp_servers": "ocspServers",
    "oidc_client_id": "oidcClientId",
    "oidc_client_secret": "oidcClientSecret",
    "oidc_discovery_ca_pem": "oidcDiscoveryCaPem",
    "oidc_discovery_url": "oidcDiscoveryUrl",
    "oidc_scopes": "oidcScopes",
    "organization_unit": "organizationUnit",
    "other_sans": "otherSans",
    "path_suffix": "pathSuffix",
    "pem_bundle": "pemBundle",
    "pem_keys": "pemKeys",
    "permitted_dns_domains": "permittedDnsDomains",
    "policy_arns": "policyArns",
    "policy_document": "policyDocument",
    "policy_identifiers": "policyIdentifiers",
    "postal_code": "postalCode",
    "postal_codes": "postalCodes",
    "private_key": "privateKey",
    "private_key_format": "privateKeyFormat",
    "private_key_id": "privateKeyId",
    "private_key_type": "privateKeyType",
    "project_id": "projectId",
    "public_key": "publicKey",
    "push_info": "pushInfo",
    "renew_increment": "renewIncrement",
    "renew_min_lease": "renewMinLease",
    "renew_statements": "renewStatements",
    "require_cn": "requireCn",
    "required_extensions": "requiredExtensions",
    "resolve_aws_unique_ids": "resolveAwsUniqueIds",
    "revocation_statements": "revocationStatements",
    "role_arns": "roleArns",
    "role_id": "roleId",
    "role_name": "roleName",
    "role_tag": "roleTag",
    "role_type": "roleType",
    "rollback_statements": "rollbackStatements",
    "rotation_period": "rotationPeriod",
    "safety_buffer": "safetyBuffer",
    "secret_id": "secretId",
    "secret_id_bound_cidrs": "secretIdBoundCidrs",
    "secret_id_num_uses": "secretIdNumUses",
    "secret_id_ttl": "secretIdTtl",
    "secret_key": "secretKey",
    "secret_type": "secretType",
    "serial_number": "serialNumber",
    "server_flag": "serverFlag",
    "service_account_email": "serviceAccountEmail",
    "skip_tls_verify": "skipTlsVerify",
    "street_address": "streetAddress",
    "street_addresses": "streetAddresses",
    "sts_endpoint": "stsEndpoint",
    "sts_role": "stsRole",
    "subscription_id": "subscriptionId",
    "supports_decryption": "supportsDecryption",
    "supports_derivation": "supportsDerivation",
    "supports_encryption": "supportsEncryption",
    "supports_signing": "supportsSigning",
    "tag_key": "tagKey",
    "tag_value": "tagValue",
    "tenant_id": "tenantId",
    "tls_max_version": "tlsMaxVersion",
    "tls_min_version": "tlsMinVersion",
    "token_bound_cidrs": "tokenBoundCidrs",
    "token_explicit_max_ttl": "tokenExplicitMaxTtl",
    "token_max_ttl": "tokenMaxTtl",
    "token_no_default_policy": "tokenNoDefaultPolicy",
    "token_num_uses": "tokenNumUses",
    "token_period": "tokenPeriod",
    "token_policies": "tokenPolicies",
    "token_reviewer_jwt": "tokenReviewerJwt",
    "token_scopes": "tokenScopes",
    "token_ttl": "tokenTtl",
    "token_type": "tokenType",
    "uri_sans": "uriSans",
    "use_csr_common_name": "useCsrCommonName",
    "use_csr_sans": "useCsrSans",
    "use_csr_values": "useCsrValues",
    "use_token_groups": "useTokenGroups",
    "user_claim": "userClaim",
    "username_format": "usernameFormat",
    "verification_ttl": "verificationTtl",
    "verify_connection": "verifyConnection",
    "wrapped_token": "wrappedToken",
    "wrapping_accessor": "wrappingAccessor",
    "wrapping_token": "wrappingToken",
    "wrapping_ttl": "wrappingTtl",
    "write_data": "writeData",
    "write_data_json": "writeDataJson",
    "write_fields": "writeFields",
}

_CAMEL_TO_SNAKE_CASE_TABLE = {
    "accessKey": "access_key",
    "accountId": "account_id",
    "addGroupAliases": "add_group_aliases",
    "allowAnyName": "allow_any_name",
    "allowBareDomains": "allow_bare_domains",
    "allowGceInference": "allow_gce_inference",
    "allowGlobDomains": "allow_glob_domains",
    "allowHostCertificates": "allow_host_certificates",
    "allowInstanceMigration": "allow_instance_migration",
    "allowIpSans": "allow_ip_sans",
    "allowLocalhost": "allow_localhost",
    "allowPlaintextBackup": "allow_plaintext_backup",
    "allowSubdomains": "allow_subdomains",
    "allowUserCertificates": "allow_user_certificates",
    "allowUserKeyIds": "allow_user_key_ids",
    "allowedClientId": "allowed_client_id",
    "allowedClientIds": "allowed_client_ids",
    "allowedCommonNames": "allowed_common_names",
    "allowedCriticalOptions": "allowed_critical_options",
    "allowedDnsSans": "allowed_dns_sans",
    "allowedDomains": "allowed_domains",
    "allowedEmailSans": "allowed_email_sans",
    "allowedExtensions": "allowed_extensions",
    "allowedNames": "allowed_names",
    "allowedOrganizationUnits": "allowed_organization_units",
    "allowedOtherSans": "allowed_other_sans",
    "allowedPolicies": "allowed_policies",
    "allowedRedirectUris": "allowed_redirect_uris",
    "allowedRoles": "allowed_roles",
    "allowedUriSans": "allowed_uri_sans",
    "allowedUsers": "allowed_users",
    "altNames": "alt_names",
    "apiHostname": "api_hostname",
    "applicationObjectId": "application_object_id",
    "authType": "auth_type",
    "autoRenew": "auto_renew",
    "awsPublicCert": "aws_public_cert",
    "azureRoles": "azure_roles",
    "baseUrl": "base_url",
    "basicConstraintsValidForNonCa": "basic_constraints_valid_for_non_ca",
    "bindSecretId": "bind_secret_id",
    "boundAccountIds": "bound_account_ids",
    "boundAmiIds": "bound_ami_ids",
    "boundAudiences": "bound_audiences",
    "boundCidrLists": "bound_cidr_lists",
    "boundCidrs": "bound_cidrs",
    "boundClaims": "bound_claims",
    "boundEc2InstanceIds": "bound_ec2_instance_ids",
    "boundGroupIds": "bound_group_ids",
    "boundIamInstanceProfileArns": "bound_iam_instance_profile_arns",
    "boundIamPrincipalArns": "bound_iam_principal_arns",
    "boundIamRoleArns": "bound_iam_role_arns",
    "boundInstanceGroups": "bound_instance_groups",
    "boundIssuer": "bound_issuer",
    "boundLabels": "bound_labels",
    "boundLocations": "bound_locations",
    "boundProjects": "bound_projects",
    "boundRegions": "bound_regions",
    "boundResourceGroups": "bound_resource_groups",
    "boundScaleSets": "bound_scale_sets",
    "boundServiceAccountNames": "bound_service_account_names",
    "boundServiceAccountNamespaces": "bound_service_account_namespaces",
    "boundServiceAccounts": "bound_service_accounts",
    "boundServicePrincipalIds": "bound_service_principal_ids",
    "boundSubject": "bound_subject",
    "boundSubnetIds": "bound_subnet_ids",
    "boundSubscriptionIds": "bound_subscription_ids",
    "boundVpcIds": "bound_vpc_ids",
    "boundZones": "bound_zones",
    "bypassOktaMfa": "bypass_okta_mfa",
    "caCertDir": "ca_cert_dir",
    "caCertFile": "ca_cert_file",
    "caChain": "ca_chain",
    "caChains": "ca_chains",
    "canonicalId": "canonical_id",
    "certName": "cert_name",
    "cidrList": "cidr_list",
    "cidrLists": "cidr_lists",
    "claimMappings": "claim_mappings",
    "clientAuths": "client_auths",
    "clientEmail": "client_email",
    "clientFlag": "client_flag",
    "clientId": "client_id",
    "clientSecret": "client_secret",
    "clientToken": "client_token",
    "codeSigningFlag": "code_signing_flag",
    "commonName": "common_name",
    "connectionUri": "connection_uri",
    "convergentEncryption": "convergent_encryption",
    "creationStatements": "creation_statements",
    "credentialType": "credential_type",
    "crlDistributionPoints": "crl_distribution_points",
    "dataJson": "data_json",
    "dbName": "db_name",
    "defaultCriticalOptions": "default_critical_options",
    "defaultExtensions": "default_extensions",
    "defaultLeaseTtlSeconds": "default_lease_ttl_seconds",
    "defaultRole": "default_role",
    "defaultStsTtl": "default_sts_ttl",
    "defaultTtl": "default_ttl",
    "defaultUser": "default_user",
    "deletionAllowed": "deletion_allowed",
    "denyNullBind": "deny_null_bind",
    "disableDelete": "disable_delete",
    "disablePeriodicTidy": "disable_periodic_tidy",
    "disableRead": "disable_read",
    "disallowReauthentication": "disallow_reauthentication",
    "disallowedPolicies": "disallowed_policies",
    "displayName": "display_name",
    "ec2Endpoint": "ec2_endpoint",
    "emailProtectionFlag": "email_protection_flag",
    "enforceHostnames": "enforce_hostnames",
    "enforcementLevel": "enforcement_level",
    "excludeCnFromSans": "exclude_cn_from_sans",
    "explicitMaxTtl": "explicit_max_ttl",
    "extKeyUsages": "ext_key_usages",
    "externalPolicies": "external_policies",
    "generateLease": "generate_lease",
    "generateSigningKey": "generate_signing_key",
    "groupId": "group_id",
    "groupName": "group_name",
    "groupsClaim": "groups_claim",
    "groupsClaimDelimiterPattern": "groups_claim_delimiter_pattern",
    "iamEndpoint": "iam_endpoint",
    "iamHttpRequestMethod": "iam_http_request_method",
    "iamRequestBody": "iam_request_body",
    "iamRequestHeaders": "iam_request_headers",
    "iamRequestUrl": "iam_request_url",
    "iamServerIdHeaderValue": "iam_server_id_header_value",
    "ignoreAbsentFields": "ignore_absent_fields",
    "inferredAwsRegion": "inferred_aws_region",
    "inferredEntityType": "inferred_entity_type",
    "insecureTls": "insecure_tls",
    "instanceId": "instance_id",
    "integrationKey": "integration_key",
    "ipSans": "ip_sans",
    "issuingCa": "issuing_ca",
    "issuingCertificates": "issuing_certificates",
    "jwksCaPem": "jwks_ca_pem",
    "jwksUrl": "jwks_url",
    "jwtSupportedAlgs": "jwt_supported_algs",
    "jwtValidationPubkeys": "jwt_validation_pubkeys",
    "keyBits": "key_bits",
    "keyIdFormat": "key_id_format",
    "keyName": "key_name",
    "keyType": "key_type",
    "keyUsages": "key_usages",
    "kubernetesCaCert": "kubernetes_ca_cert",
    "kubernetesHost": "kubernetes_host",
    "latestVersion": "latest_version",
    "leaseDuration": "lease_duration",
    "leaseStartTime": "lease_start_time",
    "leaseStarted": "lease_started",
    "listingVisibility": "listing_visibility",
    "maxJwtExp": "max_jwt_exp",
    "maxLeaseTtlSeconds": "max_lease_ttl_seconds",
    "maxPathLength": "max_path_length",
    "maxRetries": "max_retries",
    "maxStsTtl": "max_sts_ttl",
    "maxTtl": "max_ttl",
    "memberEntityIds": "member_entity_ids",
    "memberGroupIds": "member_group_ids",
    "minAvailableVersion": "min_available_version",
    "minDecryptionVersion": "min_decryption_version",
    "minEncryptionVersion": "min_encryption_version",
    "minSecondsRemaining": "min_seconds_remaining",
    "mountAccessor": "mount_accessor",
    "mysqlAurora": "mysql_aurora",
    "mysqlLegacy": "mysql_legacy",
    "mysqlRds": "mysql_rds",
    "noDefaultPolicy": "no_default_policy",
    "noParent": "no_parent",
    "noStore": "no_store",
    "numUses": "num_uses",
    "ocspServers": "ocsp_servers",
    "oidcClientId": "oidc_client_id",
    "oidcClientSecret": "oidc_client_secret",
    "oidcDiscoveryCaPem": "oidc_discovery_ca_pem",
    "oidcDiscoveryUrl": "oidc_discovery_url",
    "oidcScopes": "oidc_scopes",
    "organizationUnit": "organization_unit",
    "otherSans": "other_sans",
    "pathSuffix": "path_suffix",
    "pemBundle": "pem_bundle",
    "pemKeys": "pem_keys",
    "permittedDnsDomains": "permitted_dns_domains",
    "policyArns": "policy_arns",
    "policyDocument": "policy_document",
    "policyIdentifiers": "policy_identifiers",
    "postalCode": "postal_code",
    "postalCodes": "postal_codes",
    "privateKey": "private_key",
    "privateKeyFormat": "private_key_format",
    "privateKeyId": "private_key_id",
    "privateKeyType": "private_key_type",
    "projectId": "project_id",
    "publicKey": "public_key",
    "pushInfo": "push_info",
    "renewIncrement": "renew_increment",
    "renewMinLease": "renew_min_lease",
    "renewStatements": "renew_statements",
    "requireCn": "require_cn",
    "requiredExtensions": "required_extensions",
    "resolveAwsUniqueIds": "resolve_aws_unique_ids",
    "revocationStatements": "revocation_statements",
    "roleArns": "role_arns",
    "roleId": "role_id",
    "roleName": "role_name",
    "roleTag": "role_tag",
    "roleType": "role_type",
    "rollbackStatements": "rollback_statements",
    "rotationPeriod": "rotation_period",
    "safetyBuffer": "safety_buffer",
    "secretId": "secret_id",
    "secretIdBoundCidrs": "secret_id_bound_cidrs",
    "secretIdNumUses": "secret_id_num_uses",
    "secretIdTtl": "secret_id_ttl",
    "secretKey": "secret_key",
    "secretType": "secret_type",
    "serialNumber": "serial_number",
    "serverFlag": "server_flag",
    "serviceAccountEmail": "service_account_email",
    "skipTlsVerify": "skip_tls_verify",
    "streetAddress": "street_address",
    "streetAddresses": "street_addresses",
    "stsEndpoint": "sts_endpoint",
    "stsRole": "sts_role",
    "subscriptionId": "subscription_id",
    "supportsDecryption": "supports_decryption",
    "supportsDerivation": "supports_derivation",
    "supportsEncryption": "supports_encryption",
    "supportsSigning": "supports_signing",
    "tagKey": "tag_key",
    "tagValue": "tag_value",
    "tenantId": "tenant_id",
    "tlsMaxVersion": "tls_max_version",
    "tlsMinVersion": "tls_min_version",
    "tokenBoundCidrs": "token_bound_cidrs",
    "tokenExplicitMaxTtl": "token_explicit_max_ttl",
    "tokenMaxTtl": "token_max_ttl",
    "tokenNoDefaultPolicy": "token_no_default_policy",
    "tokenNumUses": "token_num_uses",
    "tokenPeriod": "token_period",
    "tokenPolicies": "token_policies",
    "tokenReviewerJwt": "token_reviewer_jwt",
    "tokenScopes": "token_scopes",
    "tokenTtl": "token_ttl",
    "tokenType": "token_type",
    "uriSans": "uri_sans",
    "useCsrCommonName": "use_csr_common_name",
    "useCsrSans": "use_csr_sans",
    "useCsrValues": "use_csr_values",
    "useTokenGroups": "use_token_groups",
    "userClaim": "user_claim",
    "usernameFormat": "username_format",
    "verificationTtl": "verification_ttl",
    "verifyConnection": "verify_connection",
    "wrappedToken": "wrapped_token",
    "wrappingAccessor": "wrapping_accessor",
    "wrappingToken": "wrapping_token",
    "wrappingTtl": "wrapping_ttl",
    "writeData": "write_data",
    "writeDataJson": "write_data_json",
    "writeFields": "write_fields",
}
