import json
import pprint

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
        utils_get_format_types['minimum'] = float(element['minimum'])

    if 'maximum' in element:
        utils_get_format_types['maximum'] = float(element['maximum'])

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

                choice = get_choice(schema_item['schema'], [])
                if choice:
                    studio_schema[-1]['spec'].append(choice)
                    # studio_schema = studio_schema + choice
                    # studio_schema = get_choice(schema_item['schema'], studio_schema)
            else:
                properties = get_properties(schema_item['schema'], []) + get_choice(schema_item['schema'], [])
                # remove_required_fields(properties)
                studio_schema.append({
                    "name": schema_item['name'],
                    "type": "collection",
                    'required': schema_item['required'],
                    "spec": properties
                })
        elif 'type_schema' in schema_item:
            if 'array' in schema_item and schema_item.get('array', False):

                studio_schema.append({
                    "type": "array",
                    "name": schema_item['name'],
                    "spec": {},
                })

                if get_format_types(schema_item).get("enum", False):
                    studio_schema[-1]['spec'] = {
                        "label": schema_item['name'],
                        "type": "select",
                        "name": schema_item['name'],
                        'required': schema_item['required'],
                        "options": list(map(lambda item: {'value': item, 'label': item},
                                            get_format_types(schema_item).get("enum", False)))
                    }
                else:
                    studio_schema[-1]['spec'] = {
                        'name': schema_item['name'],
                        'type': get_type(schema_item['type_schema']),
                        'required': schema_item['required'],
                    }

            else:
                if get_format_types(schema_item).get("enum", False):
                    studio_schema.append({
                        "label": schema_item['name'],
                        "type": "select",
                        "name": schema_item['name'],
                        'required': schema_item['required'],
                        "options": list(map(lambda item: {'value': item, 'label': item},
                                            get_format_types(schema_item).get("enum", False)))
                    })
                else:
                    studio_schema.append({
                        'name': schema_item['name'],
                        'type': get_type(schema_item['type_schema']),
                        'required': schema_item['required'],
                    })
    return studio_schema


def get_label(data):
    if isinstance(data, list):
        for d in data:
            return get_label(d)
    else:
        return data['name']


def get_choice_rec(choice, studio_schema):
    import uuid
    from flatten_dict import flatten, unflatten  # type: ignore
    # todo need to improve this function. i think there has bug but not sure
    # group = any(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    count_of_lists = sum(isinstance(schema_item_choice_item, list) for schema_item_choice_item in choice)
    if count_of_lists == len(choice):
        for schema_item_choice in choice:
            studio_schema.append({
                "label": "select One",
                "type": "select",
                "name": f'remove_{str(uuid.uuid4())}',
                "options": []
            })
            try:
                if isinstance(schema_item_choice, dict):
                    studio_schema[-1]['options'].append({
                        'value': str(uuid.uuid4()),
                        'label': get_label(schema_item_choice),
                        'nested': get_properties([schema_item_choice], [])
                    })

                else:
                    for schema_item_choice_item in schema_item_choice:
                        studio_schema[-1]['options'].append({
                            'value': str(uuid.uuid4()),
                            'label': get_label(schema_item_choice_item),
                            'nested': get_properties([schema_item_choice_item], [])
                        })
            except  Exception as ex:
                print(schema_item_choice)
    else:
        studio_schema.append({
            "label": "select One",
            "type": "select",
            "name": f'remove_{str(uuid.uuid4())}',
            "options": []
        })

        for schema_item_choice in choice:
            if isinstance(schema_item_choice, dict):
                studio_schema[-1]['options'].append({
                    'value': str(uuid.uuid4()),
                    'label': get_label(schema_item_choice),
                    'nested': get_properties([schema_item_choice], [])
                })
            else:
                label = ""
                for schema_item_choice_item in schema_item_choice:
                    label = label + " " + schema_item_choice_item['name']
                    # flattened_dict: dict = flatten(schema_item_choice_item, reducer="underscore")
                    studio_schema[-1]['options'].append({
                        'value': str(uuid.uuid4()),
                        'label': label,
                        'nested': get_properties([schema_item_choice_item], [])
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


def snake_to_pascal_case(snake_str):
    words = snake_str.split('_')
    pascal_words = [word.capitalize() for word in words]
    return ' '.join(pascal_words)


def mainOneFile():
    studio_doc = {

    }

    def update_generate_studio_doc(schema, name):
        studio_doc[name] = schema
        return studio_doc

    for key in STUDIO_CONVERT_ALL:

        with open(key, 'r') as file:
            schema_oci = json.load(file)

        for request in schema_oci:
            if request['type'] == 'core:OCIRequest':
                array = []
                get_properties(request['schema'], array)

                choice = []
                get_choice(request['schema'], choice)

                update_generate_studio_doc(array + choice, name=request['name'])

    file = open('converted-data/v2/studio/studio.json', "w")

    # Write content to the file
    def fix_required(schema):
        if not isinstance(schema, dict):
            return None
        schema_items = schema.copy().items()
        for key, value in schema_items:
            if key == 'spec':
                data_dict = dict(schema_items)
                if 'required' in data_dict and not data_dict['required']:
                    for item_value in data_dict['spec']:
                        if 'required' in item_value:
                            item_value.pop('required')
                # exit()
            if isinstance(value, dict):
                fix_required(value)
            if isinstance(value, list):
                for v in value:
                    if isinstance(v, dict):
                        fix_required(v)

    fix_required(studio_doc)
    file.write(json.dumps(studio_doc))

    # Close the file
    file.close()


mainOneFile()

# with open('studio.json', 'r') as file:
#     schema_oci = json.load(file)
#     print(len(schema_oci))
# for key in STUDIO_CONVERT_ALL:
#     main(key, STUDIO_CONVERT_ALL[key])