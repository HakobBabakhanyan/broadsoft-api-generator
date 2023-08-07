import json

import humps

from constants import CONST_TYPES_STUDIO, CONST_TYPE_FORMATS, STUDIO_CONVERT_ALL, OCI_SCHEMA_JSON_FILE_NAME, \
    SWAGGER_CONVERT_ALL


# todo BUG /UserAnnouncementFileAddRequest  (Enterprise - abstract)
# todo BUG searchCriteriaUserLastName  need to be array now object

def get_type(const_type: str):
    """
    return the const key
    :param const_type:
    :return:
    """
    return CONST_TYPES_STUDIO[const_type] if const_type in CONST_TYPES_STUDIO else const_type


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
        utils_get_format_types['minimum'] = int(element['minimum'])

    if 'maximum' in element:
        utils_get_format_types['maximum'] = int(element['maximum'])

    if 'enum' in element:
        utils_get_format_types['enum'] = element['enum']

    return utils_get_format_types


def get_properties(schema, studio_schema):
    for schema_item in schema:
        if schema_item is None:
            continue
        if isinstance(schema_item, list):
            studio_schema = get_properties(schema_item, studio_schema)
        elif 'schema' in schema_item:
            if 'array' in schema_item and schema_item.get('array', False):
                studio_schema.append({
                    "type": "array",
                    "name": schema_item['name'],
                    "spec": get_properties(schema_item['schema'], []),
                })
                # swagger_schema[schema_item['name']] = {
                #     'type': 'array',
                #     'required': schema_item.get('required', False),
                #     "items": {
                #         "type": "object",
                #         'properties': get_properties(schema_item['schema'], {}),
                #     },
                #     # **get_choice(schema_item['schema'], {}),
                #     # **get_format_types(schema_item)
                # }
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

                properties = get_properties(schema_item['schema'], [])
                # remove_required_fields(properties)
                studio_schema.append({
                    "name": schema_item['name'],
                    "type": "collection",
                    "spec": properties
                })
        elif 'type_schema' in schema_item:
            studio_schema.append({
                'name': schema_item['name'],
                'type': get_type(schema_item['type_schema']),
                'required': schema_item['required'],
            })
            # swagger_schema[schema_item['name']] = {
            #     'required': schema_item['required'],
            #     'type': get_type(schema_item['type_schema']),
            #     **get_type_and_format(schema_item['type_schema']),
            #     **get_format_types(schema_item)
            # }
    return studio_schema


def get_choice_rec(choice, studio_schema):
    import uuid
    # todo need to improve this function. i think there has bug but not sure
    # group = any(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    count_of_lists = sum(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    if count_of_lists == len(choice):
        # swagger_schema['anyOf'] = []
        return studio_schema
        studio_schema.append({
            "label": "select One",
            "type": "select",
            "options": []
        })
        for schema_item_choice in choice:

            if isinstance(schema_item_choice, dict):
                continue
                studio_schema[-1]['options'].append({
                    'value': str(uuid.uuid4()),
                    'nested': get_properties([schema_item_choice], [])
                })
            else:
                studio_schema[-1]['options'].append({
                    'value': str(uuid.uuid4()),
                    'nested': {
                        "label": "select One",
                        "type": "select",
                        "options": []
                    }
                })

                for schema_item_choice_item in schema_item_choice:
                    studio_schema[-1]['options'][-1]['nested']['options'].append({
                        'value': str(uuid.uuid4()),
                        'nested': get_properties([schema_item_choice_item], [])
                    })
                    # swagger_schema['anyOf'][-1]['oneOf'].append({
                    #     'type': 'object',
                    #     # 'required': schema_item_choice[
                    #     #     'required'] if 'required' in schema_item_choice else False,
                    #     'properties': get_properties([schema_item_choice_item], {})
                    # })
    else:
        studio_schema.append({
            "label": "select One",
            "type": "select",
            "options": []
        })
        for schema_item_choice in choice:
            group = any(
                isinstance(schema_item_choice_item, list) for schema_item_choice_item in schema_item_choice)
            if group and len(schema_item_choice) > 1:
                for schema_item_choice_item in schema_item_choice:
                    continue
                    studio_schema[-1]['options'].append({
                        'value': str(uuid.uuid4()),
                        'nested': get_properties([schema_item_choice_item], [])
                    })
                    # studio_schema[-1]['options'].append({
                    #     'name': 'object',
                    #     # 'required': schema_item_choice_item[
                    #     #     'required'] if 'required' in schema_item_choice_item else False,
                    #     'spec': get_properties([schema_item_choice_item], [])
                    # })
            else:
                studio_schema[-1]['options'].append({
                    'value': str(uuid.uuid4()),
                    'nested': get_properties([schema_item_choice], [])
                })
    return studio_schema


def get_choice(schema, studio_schema):
    for schema_item in schema:
        if schema_item is None:
            continue
        if isinstance(schema_item, list):
            studio_schema = get_choice(schema_item, studio_schema)
        elif 'choice' in schema_item:
            studio_schema = get_choice_rec(schema_item['choice'], studio_schema)
    return studio_schema


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


def main(schema_file_name, studio_file_name):
    studio_doc = {}

    def update_generate_swagger_doc(schema, name):
        studio_doc[name] = schema
        return studio_doc

    with open(schema_file_name, 'r') as file:
        schema_oci = json.load(file)

    for request in schema_oci:
        if request['type'] == 'core:OCIRequest':
            array = []
            get_properties(request['schema'], array)

            choice = []
            get_choice(request['schema'], choice)
            update_generate_swagger_doc(array + choice, name=request['name'])

    file = open(studio_file_name, "w")

    # Write content to the file
    file.write(json.dumps(studio_doc))

    # Close the file
    file.close()


for key in STUDIO_CONVERT_ALL:
    print(key)
    main(key, STUDIO_CONVERT_ALL[key])
# main()
