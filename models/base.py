from flask_restx import fields

api_root_information = {
                        'resource_url': fields.String(required=True, description="The URL of the resource queried by the API"),
                        'organization': fields.String(required=True, description="Organization owning queried resource"),
                        'organization_url': fields.String(required=True, decription="The URL of the organization owning queried resource"),
                        'description': fields.String(required=True, description="Description of resource"),
                        'endpoint': fields.String(required=True, description="Root endpoint for the resouce API"),
                        'version': fields.String(description="tagged release version of the resource API")
                        }

