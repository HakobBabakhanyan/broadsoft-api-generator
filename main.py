import json
import re
import humps
import xmltodict
from collections import OrderedDict
from constants import CONST_TYPES

file_path_schemas = {
    'Deprecated24AS': 'ocip_schema/OCISchemaDeprecated24AS.xsd',
    'Deprecated': 'ocip_schema/OCISchemaDeprecated.xsd',
    'DeprecatedAs': 'ocip_schema/OCISchemaDeprecatedAS.xsd',
    'Group': 'ocip_schema/OCISchemaGroup.xsd',
    'User': 'ocip_schema/OCISchemaUser.xsd',
    'Enterprise': 'ocip_schema/OCISchemaEnterprise.xsd',
    'Reseller': 'ocip_schema/OCISchemaReseller.xsd',
    'System': 'ocip_schema/OCISchemaSystem.xsd',
    'ServiceProvider': 'ocip_schema/OCISchemaServiceProvider.xsd',
    'Login': 'ocip_schema/OCISchemaLogin.xsd',
    # 'bug': 'ocip_schema/bugs.xsd',
}
folder_path_schemas = {
    "Services":'ocip_schema/Services'
}



# output_file = 'converted-data/group.json'


def get_format_types(element):
    utils_get_format_types = {}

    if 'xs:enumeration' in element:
        utils_get_format_types['enum'] = []
        if isinstance(element['xs:enumeration'], list):
            for enumeration in element['xs:enumeration']:
                utils_get_format_types['enum'].append(enumeration['@value'])
        else:
            utils_get_format_types['enum'].append(element['xs:enumeration']['@value'])
    if 'xs:minLength' in element:
        utils_get_format_types['minLength'] = int(element['xs:minLength']['@value'])

    if 'xs:maxLength' in element:
        utils_get_format_types['maxLength'] = int(element['xs:maxLength']['@value'])

    if 'xs:minInclusive' in element:
        utils_get_format_types['minimum'] = float(element['xs:minInclusive']['@value'])

    if 'xs:maxInclusive' in element:
        utils_get_format_types['maximum'] = float(element['xs:maxInclusive']['@value'])

    return utils_get_format_types


def get_schema_data_types():
    """
    this function get the data types in array
    :return:
    """
    with open('ocip_schema/OCISchemaDataTypes.xsd', 'r') as file:
        oci_schema_data_types = xmltodict.parse(file.read())
    with open('ocip_schema/OCISchemaSearchCriteria.xsd', 'r') as file:
        oci_schema_search_criteria_types = xmltodict.parse(file.read())
    with open('ocip_schema/OCISchemaSortCriteria.xsd', 'r') as file:
        oci_schema_sort_criteria_types = xmltodict.parse(file.read())

    return [oci_schema_data_types, oci_schema_search_criteria_types, oci_schema_sort_criteria_types]


schema_data_types = get_schema_data_types()


def get_file_content(tags):
    """
    get file content
    :return: AnyStr
    """
    # Read the content of the file
    content = open(f'converted-data/v2/base/{humps.kebabize(tags[0])}.json', "r").read()

    # Close the file

    # Print the content
    return content


def get_object_schema_element(element):
    """
    get element type and schema if exists
    :param element:
    :return:
    """
    # todo change logic

    if element.get('@type'):
        return {
            'name': element.get('@name'),
            'required': True if element.get('@minOccurs', "1") >= "1" else False,
            'array': True if element.get('@maxOccurs') == "unbounded" or int(
                element.get('@maxOccurs', 0)) > 1 else False,
            'type': element.get('@type')
        }
    elif 'xs:simpleType' in element and element['xs:simpleType']['xs:restriction']['@base']:
        return {
            'name': element.get('@name'),
            'required': True if element.get('@minOccurs', "1") >= "1" else False,
            'array': True if element.get('@maxOccurs') == "unbounded" or int(
                element.get('@maxOccurs', 0)) > 1 else False,
            'type': element['xs:simpleType']['xs:restriction']['@base'],
            **get_format_types(element['xs:simpleType']['xs:restriction'])
        }
    elif element.get('xs:complexType'):
        return {
            'name': element.get('@name'),
            'type': None,
            'required': True if element.get('@minOccurs', "1") >= "1" else False,
            'array': True if element.get('@maxOccurs') == "unbounded" or int(
                element.get('@maxOccurs', 0)) > 1 else False,
            'schema': get_object_schema_rec(element.get('xs:complexType'), [])
        }
    else:
        # todo only this case 'fileRebuildImmediate' I don't now what is the right type
        return {
            'name': element.get('@name'),
            'required': True if element.get('@minOccurs', "1") >= "1" else False,
            'array': True if element.get('@maxOccurs') == "unbounded" or int(
                element.get('@maxOccurs', 0)) > 1 else False,
            'type': 'xs:int'
        }


def get_object_schema_rec(extensions: dict, body: list):
    """
    get the object schema recursive and beater view
    :param extensions:
    :param body:
    :return:
    """
    if isinstance(extensions, list):
        # this part for case where need group elements example choice
        for index, extension in enumerate(extensions):
            body.append([])
            get_object_schema_rec(extension, body[-1])
    else:
        if 'xs:sequence'in extensions and extensions.get('xs:sequence') is None:
            base = getTypeXSD(extensions.get('@base'), schema_data_types)
            body.append(base)

        if extensions.get('xs:element'):
            if isinstance(extensions.get('xs:element'), list):
                for element in extensions.get('xs:element'):
                    body.append(get_object_schema_element(element))
            else:
                element = extensions.get('xs:element')
                body.append(get_object_schema_element(element))
        if extensions.get('xs:sequence'):
            #  todo maybe sequence not uniq in the same group
            body.append([])
            get_object_schema_rec(extensions.get('xs:sequence'), body[-1])

        if extensions.get('xs:choice'):
            body.append({'choice': []})
            get_object_schema_rec(extensions.get('xs:choice'), body[-1]['choice'])

        return body

    return body


def write_output_file_content(content, tags):
    """
    write the file content
    :param content:
    :param tags:
    :return:
    """
    # Open the file in write mode
    write_file = open(f'./converted-data/v2/base/{humps.kebabize(tags[0])}.json', "w")

    # Write content to the file
    write_file.write(content)

    # Close the file
    write_file.close()


def xml_schema_to_json_schema(xml_object: dict, xml_data_str, tags, add):
    """
    the main function convertor # todo need more info

    :param xml_object:
    :param xml_data_str:
    :param tags:
    :return:
    """

    xs_schema = xml_object.get('xs:schema')
    complex_types = xs_schema.get('xs:complexType')
    if not complex_types:
        return
    for complex_type in complex_types:
        body = []

        try:
            complex_content_extension = complex_type.get('xs:complexContent').get('xs:extension')
        except AttributeError:
            complex_content_extension = {}

        if complex_content_extension.get('@base') != 'core:OCIRequest':
            continue

        http_request = {
        'name': complex_type.get('@name'),
        'tags': tags,
        'documentation': complex_type.get('xs:annotation').get('xs:documentation') if complex_type.get("xs:annotation") else "",
        'type': complex_content_extension.get('@base'),
        'schema': get_object_schema_rec(complex_content_extension, body)
        }

        for schema in http_request['schema']:
            get_schema_rec(schema, xml_object)
            """
                SORT START
            """
        # match = re.search(fr'<xs:complexType name="{http_request["name"]}".*>(.*?\s)+?</xs:complexType>', xml_data_str)
        # if match:
        #     extracted_content = match.group(0)
        #     elementGroups = re.findall(fr'<xs:element name="(\w+)"', extracted_content)
        #     http_request['sort'] = elementGroups
        """
                        SORT END
        """
        http_requests = json.loads(get_file_content(tags))
        http_requests.append(http_request)

        write_output_file_content(json.dumps(http_requests), tags)


def get_sort(xml_data_str, name):
    """
    this function return array the info about right sorting
    :param xml_data_str:
    :param name:
    :return:
    """
    match = re.search(fr'<xs:complexType name="{name}".*>(.*?\s)+?</xs:complexType>', xml_data_str)
    if match:
        extracted_content = match.group(0)
        elementGroups = re.findall(fr'<xs:element name="(\w+)"', extracted_content)
        return elementGroups
    else:
        return None


# def get_schema_data_types_xsd():
#     with open('ocip_schema/OCISchemaDataTypes.xsd', 'r') as file:
#         xml_data = file.read()
#     return xml_data


def getTypeXSD(type_name, schema_data_types):
    for schema_data_type in schema_data_types:
        schema_data_type_schema = schema_data_type['xs:schema']
        for complex_type in schema_data_type_schema['xs:complexType']:
            if complex_type["@name"] == type_name:
                body = []
                if 'xs:complexContent' in complex_type:
                    extension = complex_type.get('xs:complexContent').get('xs:extension')
                    if extension is None:
                        extension = complex_type.get('xs:complexContent').get('xs:restriction').get('xs:sequence')
                    return get_object_schema_rec(extension, body)
                return get_object_schema_rec(complex_type, body)

        if 'xs:simpleType' in schema_data_type_schema:
            if isinstance(schema_data_type_schema['xs:simpleType'], list):
                for complex_type in schema_data_type_schema['xs:simpleType']:
                    if complex_type["@name"] == type_name:
                        return {
                        'type': complex_type['xs:restriction']['@base'],
                        **get_format_types(element=complex_type['xs:restriction'])
                        }
            else:
                complex_type = schema_data_type_schema['xs:simpleType']
                if complex_type["@name"] == type_name:
                    return {
                        'type': complex_type['xs:restriction']['@base'],
                        **get_format_types(element=complex_type['xs:restriction'])
                    }
    return type_name


def get_type_schema(type_name, xml_main):
    """
    The function get all existing schema in object recursive

    :param type_name:
    :param xml_main:
    :return:
    """
    schema_main = xml_main['xs:schema']
    for complex_type in schema_main['xs:complexType']:
        if complex_type["@name"] == type_name:
            body = []
            return get_object_schema_rec(complex_type, body)

    if 'xs:simpleType' in schema_main and isinstance(schema_main['xs:simpleType'], list):
        for complex_type in schema_main['xs:simpleType']:
            if complex_type["@name"] == type_name:
                return complex_type['xs:restriction']['@base']
    else:
        if 'xs:simpleType' in schema_main and schema_main['xs:simpleType']["@name"] == type_name:
            return schema_main['xs:simpleType']['xs:restriction']['@base']
    #  bug getting enum continue 

    return type_name



def get_type_and_sort(item, xml_main):
    """
    the function get type name and right sorting
    :param item:
    :param xml_main:
    :return:
    """
    if 'type' in item and item['type']:
        type_xsd = get_type_schema(type_name=item['type'], xml_main=xml_main)


        if isinstance(type_xsd, str) and type_xsd not in CONST_TYPES:
            type_xsd = getTypeXSD(type_name=item['type'], schema_data_types=schema_data_types)
        if isinstance(type_xsd, str):
            type_xsd = getTypeXSD(type_name=item['type'], schema_data_types=[xml_main])
        if 'type' in type_xsd and isinstance(type_xsd['type'], str):
            item['type_schema'] = type_xsd['type']
            item.update({key: type_xsd[key] for key in type_xsd if key not in item})
        elif isinstance(type_xsd, str):
            item['type_schema'] = type_xsd  # todo change logic and  remove  this case type' in type_xsd
        else:
            item['schema'] = type_xsd
            if not type_xsd:
                type_xsd = getTypeXSD(type_name=item['type'], schema_data_types=[xml_main])
                item['schema'] = type_xsd
            # todo  get_schema_data_types_xsd return only  one data file need all
            """
            SORT START
            """
            # item['sort'] = get_sort(get_schema_data_types_xsd(), item['type'])
            """
            SORT START
            """

    return item


def get_schema_rec(schema, xml_main):
    for item in schema:
        if isinstance(item, dict):
            item = get_type_and_sort(item, xml_main)
            if 'schema' in item:
                for item_schema in item['schema']:
                    if item_schema is not None:
                        get_schema_rec(item_schema, xml_main)
            elif 'choice' in item:
                for item_schema in item['choice']:
                    if isinstance(item_schema, list):
                        get_schema_rec(item_schema, xml_main)
                    else:
                        get_schema_rec([item_schema], xml_main)
        elif isinstance(item, list):
            get_schema_rec(item, xml_main)
        elif 'choice' == item:
            get_schema_rec(schema['choice'], xml_main)
    return schema


import os

def run_files():
    print('run_files')
    for file_path_schema in file_path_schemas:
        with open(file_path_schemas[file_path_schema], 'r') as file:
            xml_data = file.read()

        os.makedirs(os.path.dirname(f'./converted-data/v2/base/{humps.kebabize(file_path_schema)}.json'), exist_ok=True)
        write_output_file_content('[]', [file_path_schema])
        xml_dict_main = xmltodict.parse(xml_data, dict_constructor=OrderedDict)

        xml_schema_to_json_schema(xml_object=xml_dict_main, xml_data_str=xml_data, tags=[f'{file_path_schema}'], add=False)
    print('end')
run_files()

def services():
    contents = os.listdir('ocip_schema/Services')
    os.makedirs(os.path.dirname(f'./converted-data/v2/base/{humps.kebabize("services")}.json'), exist_ok=True)
    write_output_file_content('[]', [f'./converted-data/v2/base/{humps.kebabize("services")}.json'])
    files = [file for file in contents if os.path.isfile(os.path.join("ocip_schema/Services", file))]

    for file_name in files:
        with open(f'./ocip_schema/Services/{file_name}', 'r') as file:
            xml_data = file.read()
        xml_dict_main = xmltodict.parse(xml_data, dict_constructor=OrderedDict)

        xml_schema_to_json_schema(xml_object=xml_dict_main, xml_data_str=xml_data, tags=[f'services'], add=True)



#         xml_data = file.read()
