import json
import re
import os
from collections import defaultdict

import yaml


models = dict()


def parse_array(value, is_nullable=False):
    items = parse_model(value)

    result = {
        'type': 'array',
        'items': items,
    }

    if is_nullable:
        result['nullable'] = True

    return result


def parse_header(header_name):
    result_name = header_name
    result = {
        'in': 'header',
        'schema': {'type': 'string'},
    }

    # required
    if result_name.endswith('!'):
        result['required'] = True
        result_name = result_name[:-1]

    result['name'] = result_name

    return result


def parse_path(name):
    return {
        'in': 'path',
        'name': name,
        'schema': {'type': 'string'},
        'required': True,
    }


def parse_query(query_name, query_type):
    result_type = query_type
    result = {
        'in': 'query',
        'name': query_name,
        'schema': {},
    }

    # required
    if result_type.endswith('!'):
        result['required'] = True
        result_type = result_type[:-1]

    result['schema']['type'] = result_type

    return result


def parse_model(input_model, is_nullable=False):
    if type(input_model) is dict:
        required = []
        properties = dict()

        for key, value in input_model.items():
            result_key = key

            is_required_key = False
            if result_key.endswith('!'):
                is_required_key = True
                result_key = result_key[:-1]

            is_nullable_key = False
            if result_key.endswith('?'):
                is_nullable_key = True
                result_key = result_key[:-1]

            if result_key.endswith('[]'):
                # array
                result_key = result_key[:-2]
                properties[result_key] = parse_array(value, is_nullable_key)
            else:
                value = parse_model(value, is_nullable_key)
                properties[result_key] = value
                if is_required_key:
                    required.append(result_key)

        result = {
            'type': 'object',
            'properties': properties,
        }

        if required:
            result['required'] = required

        if is_nullable:
            result['nullable'] = True

        return result

    if type(input_model) is str:
        result_string = input_model
        result = dict()
        # enum
        enum_match = re.search(r'\[.*\]', result_string)
        if enum_match:
            enum_string = enum_match.group(0)
            result['enum'] = yaml.load(enum_string, Loader=yaml.Loader)
            result_string = result_string.replace(enum_string, '')

        # response modelreference
        if result_string.startswith('$'):
            result_string = result_string[1:]
            result.update(models[result_string])
            return result

        result['type'] = result_string
        return result


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(f'{dir_path}/api-doc.yml', 'r') as input_stream, open(f'{dir_path}/build/swagger.json', 'w') as output_stream:
        input_data = yaml.load(input_stream, Loader=yaml.FullLoader)
        output_data = {
            'openapi': '3.0.0',
            'info': {
                'version': 'REST',
                'title': input_data['title'],
            },
            'paths': defaultdict(dict),
        }

        for model_name, model_data in input_data['models'].items():
            models[model_name] = parse_model(model_data)

        for category_name, category_data in input_data['handlers'].items():
            for handler_name, handler_data in category_data.items():
                method, path = handler_name.split()
                method = method.lower()
                output_path = output_data['paths'][path]
                output_path[method] = defaultdict(dict)
                output_path[method]['tags'] = [category_name]

                if handler_data.get('deprecated'):
                    output_path[method]['deprecated'] = True

                # parameters
                output_path[method]['parameters'] = []
                parameters = output_path[method]['parameters']

                ## headers
                for header in handler_data.get('headers', []):
                    parameters.append(parse_header(header))

                ## path
                for match in re.findall(r'{(.*)}', handler_name):
                    parameters.append(parse_path(match))

                ## query
                for query_name, query_type in handler_data.get('query', {}).items():
                    parameters.append(parse_query(query_name, query_type))

                # request
                request = handler_data.get('request', None)
                if request:
                    schema = parse_model(request)
                    output_path[method]['requestBody'] = {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': schema,
                            },
                        },
                    }

                # response
                schema = parse_model(handler_data['response'])
                output_path[method]['responses'] = {
                    '200': {
                        'description': 'success',
                        'content': {
                            'application/json': {
                                'schema': schema,
                            },
                        },
                    },
                }

        output_stream.write(json.dumps(output_data, indent=2))
