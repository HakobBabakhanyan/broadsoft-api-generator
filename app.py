import os
from flask import Flask, send_from_directory, render_template
from swagger_ui import api_doc
import json

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')


# @app.route('/<path:path>')
# def serve_static(path):
#
#     return send_from_directory('swagger_ui', path)


def collapse_all_operations(spec_file_path):
    with open(spec_file_path, 'r') as file:
        spec = json.load(file)

    for path in spec['paths'].values():
        for operation in path.values():
            operation['collapsed'] = True

    with open(spec_file_path, 'w') as file:
        json.dump(spec, file, indent=2)


if __name__ == '__main__':
    swagger_json_path = './data.json'
    parameters = {
        'docExpansion': 'false',
        'filter': 'true',
        # 'maxDisplayedTags': 1,
    }

    api_doc(app, config_path=swagger_json_path, parameters=parameters)
    api_doc(app, config_path='converted-data/v1/swagger-doc-group.json', parameters=parameters, url_prefix='/api/doc/group')
    api_doc(app, config_path='converted-data/v1/swagger-doc-login.json', parameters=parameters, url_prefix='/api/doc/login')
    api_doc(app, config_path='converted-data/v1/swagger-doc-user.json', parameters=parameters, url_prefix='/api/doc/user')
    api_doc(app, config_path='converted-data/v1/swagger-doc-enterprise.json', parameters=parameters, url_prefix='/api/doc/enterprise')
    api_doc(app, config_path='converted-data/v1/swagger-doc-deprecated.json', parameters=parameters, url_prefix='/api/doc/deprecated')
    api_doc(app, config_path='converted-data/v1/swagger-doc-deprecated24-as.json', parameters=parameters, url_prefix='/api/doc/deprecated24-as')
    app.run(port=5000)
