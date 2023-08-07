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
    'converted-data/group.json':'converted-data/swagger-doc-group.json',
    'converted-data/user.json':'converted-data/swagger-doc-user.json',
    'converted-data/login.json':'converted-data/swagger-doc-login.json',
    'converted-data/deprecated.json':'converted-data/swagger-doc-deprecated.json',
    'converted-data/deprecated24-as.json':'converted-data/swagger-doc-deprecated24-as.json',
    'converted-data/enterprise.json':'converted-data/swagger-doc-enterprise.json',
    'converted-data/deprecated-as.json':'converted-data/swagger-doc-deprecated-as.json',
    'converted-data/reseller.json':'converted-data/swagger-doc-reseller.json',
    'converted-data/system.json':'converted-data/swagger-doc-system.json',
    # 'converted-data/bug.json':'converted-data/swagger-doc-bug.json',
}

STUDIO_CONVERT_ALL = {
    # 'converted-data/group.json':'converted-data/swagger-doc-group.json',
    'converted-data/user.json':'converted-data/studio-doc-user.json',
    # 'converted-data/login.json':'converted-data/swagger-doc-login.json',
    # 'converted-data/deprecated.json':'converted-data/swagger-doc-deprecated.json',
    # 'converted-data/deprecated24-as.json':'converted-data/swagger-doc-deprecated24-as.json',
    # 'converted-data/enterprise.json':'converted-data/swagger-doc-enterprise.json',
    # 'converted-data/deprecated-as.json':'converted-data/swagger-doc-deprecated-as.json',
    # 'converted-data/reseller.json':'converted-data/swagger-doc-reseller.json',
    # 'converted-data/system.json':'converted-data/swagger-doc-system.json',
    # 'converted-data/bug.json':'converted-data/swagger-doc-bug.json',
}

