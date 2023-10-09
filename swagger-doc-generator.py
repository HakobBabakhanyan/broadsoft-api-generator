import json

import humps

from constants import CONST_TYPES, CONST_TYPE_FORMATS, SWAGGER_FILE_NAME, OCI_SCHEMA_JSON_FILE_NAME, SWAGGER_CONVERT_ALL, SWAGGER_CONVERT_V2_ALL


# todo BUG /UserAnnouncementFileAddRequest  (Enterprise - abstract)
# todo BUG searchCriteriaUserLastName  need to be array now object

def get_type(const_type: str):
    """
    return the const key
    :param const_type:
    :return:
    """
    return CONST_TYPES[const_type] if const_type in CONST_TYPES else const_type


def get_type_and_format(const_type: str):
    """
    return the const key
    :param const_type:
    :return:
    """
    return CONST_TYPE_FORMATS[const_type] if const_type in {"format": CONST_TYPE_FORMATS} else {}


def get_format_types(element):
    utils_get_format_types = {}

    if 'minLength' in element:
        utils_get_format_types['minLength'] = int(element['minLength'])

    if 'maxLength' in element:
        utils_get_format_types['maxLength'] = int(element['maxLength'])

    if 'minimum' in element:
        utils_get_format_types['minimum'] = float(element['minimum'])

    if 'maximum' in element:
        utils_get_format_types['maximum'] = float(element['maximum'])

    if 'enum' in element:
        utils_get_format_types['enum'] = element['enum']

    return utils_get_format_types


def get_properties(schema, swagger_schema):
    for schema_item in schema:
        if schema_item is None:
            continue
        if isinstance(schema_item, list):
            swagger_schema = get_properties(schema_item, swagger_schema)
        elif 'schema' in schema_item:
            if 'array' in schema_item and schema_item.get('array', False):
                print(schema_item)
                swagger_schema[schema_item['name']] = {
                    'type': 'array',
                    'required': schema_item.get('required', False),
                    "items": {
                        "type": "object",
                        'properties': get_properties(schema_item['schema'], {}),
                        **get_choice(schema_item['schema'], {}),
                    },
                    # **get_choice(schema_item['schema'], {}),
                    # **get_format_types(schema_item)
                }
            else:
                # def remove_required_fields(swagger_dict):
                #     keys_to_remove = []
                #     for key, value in swagger_dict.items():
                #         if isinstance(value, dict) and value.get("required", False):
                #             keys_to_remove.append(key)
                #     for key in keys_to_remove:
                #         swagger_dict.pop(key, None)
                #
                #     for value in swagger_dict.values():
                #         if isinstance(value, dict) and "properties" in value:
                #             remove_required_fields(value["properties"])

                properties = get_properties(schema_item['schema'], {})
                # remove_required_fields(properties)
                swagger_schema[schema_item['name']] = {
                    'type': 'object',
                    'required': schema_item.get('required', False),
                    'properties': properties,
                    **get_choice(schema_item['schema'], {}),
                    **get_format_types(schema_item)
                }
        elif 'type_schema' in schema_item:
            if 'array' in schema_item and schema_item.get('array', False):
                print(schema_item)
                swagger_schema[schema_item['name']] = {
                    'type': 'array',
                    'required': schema_item.get('required', False),
                    "items": {
                        "type": "string",
                        **get_format_types(schema_item)
                    },
                    # **get_choice(schema_item['schema'], {}),
                    # **get_format_types(schema_item)
                }
            else:
                swagger_schema[schema_item['name']] = {
                    'required': schema_item['required'],
                    'type': get_type(schema_item['type_schema']),
                    **get_type_and_format(schema_item['type_schema']),
                    **get_format_types(schema_item)
                }
    return swagger_schema

def get_choice_rec(choice, swagger_schema):
    # todo need to improve this function. i think there has bug but not sure
    # group = any(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    count_of_lists = sum(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    if count_of_lists == len(choice):
        swagger_schema['anyOf'] = []
        for schema_item_choice in choice:
            swagger_schema['anyOf'].append({
                'oneOf': [],
            })
            if isinstance(schema_item_choice, dict):
                swagger_schema['anyOf'][-1]['oneOf'].append({
                    'type': 'object',
                    # 'required': schema_item_choice['required'],
                    'properties': get_properties([schema_item_choice], {})
                })
            else:
                for schema_item_choice_item in schema_item_choice:
                    swagger_schema['anyOf'][-1]['oneOf'].append({
                        'type': 'object',
                        # 'required': schema_item_choice[
                        #     'required'] if 'required' in schema_item_choice else False,
                        'properties': get_properties([schema_item_choice_item], {})
                    })
    else:
        swagger_schema['oneOf'] = []
        for schema_item_choice in choice:
            group = any(
                isinstance(schema_item_choice_item, list) for schema_item_choice_item in schema_item_choice)
            if group and len(schema_item_choice) > 1:
                for schema_item_choice_item in schema_item_choice:
                    swagger_schema['oneOf'].append({
                        'type': 'object',
                        # 'required': schema_item_choice_item[
                        #     'required'] if 'required' in schema_item_choice_item else False,
                        'properties': get_properties([schema_item_choice_item], {})
                    })
            else:
                swagger_schema['oneOf'].append({
                    'type': 'object',
                    'properties': get_properties([schema_item_choice], {})
                })
    return swagger_schema
def get_choice(schema, swagger_schema):
    for schema_item in schema:
        if schema_item is None:
            continue
        if isinstance(schema_item, list):
            swagger_schema = get_choice(schema_item, swagger_schema)
        elif 'choice' in schema_item:
            swagger_schema = get_choice_rec(schema_item['choice'], swagger_schema)
    return swagger_schema


def remove_empty_one_of(data):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == "oneOf" and isinstance(value, list) and not value:
                del data[key]
            else:
                remove_empty_one_of(value)
    elif isinstance(data, list):
        for item in data:
            remove_empty_one_of(item)


def main(schema_file_name, swagger_file_name):
    swagger_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "Group Properties API",
            "version": "1.0.0"
        },
         "servers": [
            {
                "description": "Lab",
                "url": "https://b7ftljz4m6.execute-api.us-west-2.amazonaws.com/v1/command"
            },
            {
                "description": "Prod",
                "url": " https://dtjdrpasm2.execute-api.us-west-1.amazonaws.com/v1/command"
            }
        ],
        "paths": {
        },
        "components": {
            "securitySchemes": {
                "basicAuth": {
                    "type": "http",
                    "scheme": "basic"
                }
            },
            "schemas": {}
        }
    }

    def update_generate_swagger_doc(schema, name, description, group=None):
        if group is None:
            group = ['defaults']
        path = {
            f'/{humps.kebabize(group[0])}/{name}': {
                'post': {
                    'tags': group,
                    'summary': name,
                    'description': description,
                    "security": [
                        {
                            "basicAuth": [],

                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f'#/components/schemas/{name}'
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": ""
                        }
                    }
                }
            }
        }
        def fix_required(schema):
            if not isinstance(schema, dict):
                return None
            schema_items = schema.copy().items()
            for key, value in schema_items:
                if key == 'properties':
                    required_array = []
                    for item_key, item_value in value.items():
                        if 'required' in item_value:
                            if item_value['required']:
                                required_array.append(item_key)
                            item_value.pop('required')
                    if len(required_array) > 0:
                        schema['required'] = required_array
                if isinstance(value, dict):
                   fix_required(value)
                if isinstance(value, list):
                    for v in value:
                        if isinstance(v, dict):
                            fix_required(v)
        fix_required(schema[name])
        swagger_doc['paths'].update(path)
        swagger_doc['components']['schemas'].update(schema)


        return swagger_doc

    with open(schema_file_name, 'r') as file:
        schema_oci = json.load(file)

    for request in schema_oci:
        if request['type'] == 'core:OCIRequest':
            objects = {}
            get_properties(request['schema'], objects)
            choice = {}
            get_choice(request['schema'], choice)
            object_schema = {
                request['name']: {
                    "type": "object",
                    "properties": objects,
                    **choice
                }
            }
            remove_empty_one_of(object_schema)
            update_generate_swagger_doc(object_schema, name=request['name'], description=request['documentation'], group=request['tags'])

    file = open(swagger_file_name, "w")

    # Write content to the file
    file.write(json.dumps(swagger_doc))

    # Close the file
    file.close()




def mainOneFile():
    swagger_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "OCI-P Rest Api",
            "version": "1.0.0"
        },
        "servers": [
            {
                "description": "Lab",
                "url": "https://b7ftljz4m6.execute-api.us-west-2.amazonaws.com/v1/command"
            },
            {
                "description": "Prod",
                "url": " https://dtjdrpasm2.execute-api.us-west-1.amazonaws.com/v1/command"
            }
        ],
        "paths": {
        },
        "components": {
            "securitySchemes": {
                "basicAuth": {
                    "type": "http",
                    "scheme": "basic",
                    "required": True
                }
            },
            "schemas": {}
        }
    }
    def update_generate_swagger_doc(schema, name, description, group=None):
        if group is None:
            group = ['defaults']
        path = {
            f'/{humps.kebabize(group[0])}/{name}': {
                'post': {
                    'tags': group,
                    'summary': name,
                    'description': description,
                    "security": [
                        {
                            "basicAuth": []
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f'#/components/schemas/{name}'
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": ''
                        }
                    }
                }
            }
        }

        def fix_required(schema):
            if not isinstance(schema, dict):
                return None
            schema_items = schema.copy().items()
            for key, value in schema_items:
                if key == 'properties':
                    required_array = []
                    for item_key, item_value in value.items():
                        if 'required' in item_value:
                            if item_value['required']:
                                required_array.append(item_key)
                            item_value.pop('required')
                    if len(required_array) > 0:
                        schema['required'] = required_array
                if isinstance(value, dict):
                    fix_required(value)
                if isinstance(value, list):
                    for v in value:
                        if isinstance(v, dict):
                            fix_required(v)

        fix_required(schema[name])
        swagger_doc['paths'].update(path)
        swagger_doc['components']['schemas'].update(schema)

        return swagger_doc

    for key in SWAGGER_CONVERT_V2_ALL:

        with open(key, 'r') as file:
            schema_oci = json.load(file)

        for request in schema_oci:
            if request['type'] == 'core:OCIRequest':
                objects = {}
                get_properties(request['schema'], objects)
                choice = {}
                get_choice(request['schema'], choice)
                object_schema = {
                    request['name']: {
                        "type": "object",
                        "properties": objects,
                        **choice
                    }
                }
                remove_empty_one_of(object_schema)
                update_generate_swagger_doc(object_schema, name=request['name'], description=request['documentation'], group=request['tags'])

    file = open('converted-data/v2/swagger/swagger.json', "w")

    # Write content to the file
    file.write(json.dumps(swagger_doc))

    # Close the file
    file.close()



# for key in SWAGGER_CONVERT_V2_ALL:
#     main(key, SWAGGER_CONVERT_V2_ALL[key])


# #
mainOneFile()