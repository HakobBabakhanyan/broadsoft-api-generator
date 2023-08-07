from flask import Flask, send_file, render_template
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Define your Swagger JSON files and their corresponding endpoints
swagger_files = {
    "user": {
        "file_path": "./converted-data/swagger-doc-user.json",
        "endpoint": "/swagger.json/user",
        "name": "swagger_ui_user",
    },
    "group": {
        "file_path": "./converted-data/swagger-doc-group.json",
        "endpoint": "/swagger.json/group",
        "name": "swagger_ui_group",
    },
    "enterprise": {
        "file_path": "./converted-data/swagger-doc-enterprise.json",
        "endpoint": "/swagger.json/enterprise",
        "name": "swagger_ui_enterprise",
    },
    "deprecated24-as": {
        "file_path": "./converted-data/swagger-doc-deprecated24-as.json",
        "endpoint": "/swagger.json/deprecated24-as",
        "name": "swagger_ui_deprecated24-as",
    },
    "deprecated": {
        "file_path": "./converted-data/swagger-doc-deprecated.json",
        "endpoint": "/swagger.json/deprecated",
        "name": "swagger_ui_deprecated",
    },
    "login": {
        "file_path": "./converted-data/swagger-doc-login.json",
        "endpoint": "/swagger.json/login",
        "name": "swagger_ui_login",
    },

    "bug": {
        "file_path": "./converted-data/swagger-doc-bug.json",
        "endpoint": "/swagger.json/bug",
        "name": "swagger_ui_bug",
    },
    # Add more Swagger JSON files here following the same format
}

# Dictionary to store SwaggerFile instances with their endpoints
swagger_instances = {}

# Endpoint to serve the Swagger JSON file
class SwaggerFile(Resource):
    def __init__(self, file_key):
        self.file_key = file_key

    def get(self):
        if self.file_key in swagger_files:
            return send_file(swagger_files[self.file_key]["file_path"])
        else:
            return {"message": "Swagger JSON file not found"}, 404

# Register Swagger JSON endpoints
for key in swagger_files:
    api.add_resource(SwaggerFile, swagger_files[key]["endpoint"], endpoint=key, resource_class_args=(key,))
    swagger_instances[key] = SwaggerFile(key)  # Create SwaggerFile instance and store in dictionary

# Create a blueprint for the Swagger UI
def create_swagger_ui_blueprint(file_key):
    return get_swaggerui_blueprint(
        f"/swagger/{file_key}",
        f"/swagger.json/{file_key}",
        config={"app_name": f"API {file_key.capitalize()}", "docExpansion": "none"}
    )

# Register Swagger UI blueprints
for key in swagger_files:
    app.register_blueprint(create_swagger_ui_blueprint(key), url_prefix=f"/swagger/{key}", name=swagger_files[key]["name"])


@app.route("/")
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
