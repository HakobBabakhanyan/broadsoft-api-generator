CONST_TYPES = {
    'xs:int': 'integer',
    'xs:token': 'string',
    'NonEmptyToken': 'string',
    'xs:boolean': 'boolean',
    'xs:NMTOKEN': 'string',
    'xs:long': 'string',
    'xs:string': 'string',
    'xs:base64Binary': 'string',
    'xs:date': 'string',
}
CONST_TYPES_STUDIO = {
    'xs:int': 'integer',
    'xs:token': 'text',
    'NonEmptyToken': 'text',
    'xs:boolean': 'boolean',
    'xs:NMTOKEN': 'string',
    'xs:long': 'text',
    'xs:string': 'text',
    'xs:base64Binary': 'text',
    'xs:date': 'text',
}

CONST_TYPE_FORMATS = {
    'xs:date': 'date',
}

SWAGGER_FILE_NAME = 'converted-data/v1/swagger-doc-group.json'

OCI_SCHEMA_JSON_FILE_NAME = 'converted-data/group.json'

SWAGGER_CONVERT_ALL = {
    # 'converted-data/group.json':'converted-data/swagger-doc-group.json',
    # 'converted-data/user.json':'converted-data/swagger-doc-user.json',
    # 'converted-data/login.json':'converted-data/swagger-doc-login.json',
    # 'converted-data/deprecated.json':'converted-data/swagger-doc-deprecated.json',
    # 'converted-data/deprecated24-as.json':'converted-data/swagger-doc-deprecated24-as.json',
    # 'converted-data/enterprise.json':'converted-data/swagger-doc-enterprise.json',
    # 'converted-data/deprecated-as.json':'converted-data/swagger-doc-deprecated-as.json',
    # 'converted-data/reseller.json':'converted-data/swagger-doc-reseller.json',
    # 'converted-data/system.json':'converted-data/swagger-doc-system.json',
    # 'converted-data/service-provider.json':'converted-data/swagger-doc-service-provider.json',
    # 'converted-data/services.json':'converted-data/swagger-doc-services.json',


    'converted-data/services-bug.json':'converted-data/swagger-doc-bug.json',
}

SWAGGER_CONVERT_V2_ALL = {
    'converted-data/v2/base/group.json':'converted-data/v2/swagger/swagger-doc-group.json',
    'converted-data/v2/base/user.json':'converted-data/v2/swagger/swagger-doc-user.json',
    'converted-data/v2/base/login.json':'converted-data/v2/swagger/swagger-doc-login.json',
    'converted-data/v2/base/deprecated.json':'converted-data/v2/swagger/swagger-doc-deprecated.json',
    'converted-data/v2/base/deprecated24-as.json':'converted-data/v2/swagger/swagger-doc-deprecated24-as.json',
    'converted-data/v2/base/enterprise.json':'converted-data/v2/swagger/swagger-doc-enterprise.json',
    'converted-data/v2/base/deprecated-as.json':'converted-data/v2/swagger/swagger-doc-deprecated-as.json',
    'converted-data/v2/base/reseller.json':'converted-data/v2/swagger/swagger-doc-reseller.json',
    'converted-data/v2/base/system.json':'converted-data/v2/swagger/swagger-doc-system.json',
    'converted-data/v2/base/service-provider.json':'converted-data/v2/swagger/swagger-doc-service-provider.json',
    'converted-data/v2/base/services.json':'converted-data/v2/swagger/swagger-doc-services.json',
}

BUG = {
    'converted-data/service-provider.json':'converted-data/swagger-doc-bug.json',
    # 'converted-data/bug.json':'converted-data/swagger-doc-bug.json',
}

STUDIO_CONVERT_ALL = SWAGGER_CONVERT_V2_ALL
