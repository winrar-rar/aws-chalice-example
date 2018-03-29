from chalice import Chalice
from chalice import CORSConfig
from chalice import CognitoUserPoolAuthorizer
from chalicelib import request_handler
import json
from urllib.parse import urlparse, parse_qs
import json

app = Chalice(app_name='aws-chalice-example')
app.debug = True

cors_config = CORSConfig(
    allow_origin = '*',
    allow_headers = ['X-Special-Header'],
    max_age = 600,
    expose_headers = ['X-Special-Header'],
    allow_credentials = True
)

authorizer = CognitoUserPoolAuthorizer(
    'Users', header = 'Authorization',
    provider_arns = ['arn:aws:cognito-idp:eu-west-1:009127507915:userpool/eu-west-1_yFwbkCuMn']
)

@app.route('/test', methods=['GET'], cors=cors_config, authorizer=authorizer)
def get_all():
    request = app.current_request.to_dict()

    if request.get('query_params'):
        return request_handler.handle_get_company(request['query_params']['Company'])
    else:
        return request_handler.handle_get_all()

@app.route('/test', methods=['POST'], content_types=['application/json'], cors=cors_config, authorizer=authorizer)
def post_item():
    data = app.current_request.json_body
    print("log: app.current_request.json_body = ")
    print(data)

    if data is None:
        print("ERROR: DATA IS NONE")
        return "ERROR: DATA IS NONE"
    
    return request_handler.handle_post_item(data)

@app.route('/test/{company}', methods=['PUT'], cors=cors_config, authorizer=authorizer)
def put_item(company):
    data = app.current_request.json_body
    print("log: app.current_request.json_body = ")
    print(data)

    if data is None:
        print("ERROR: DATA IS NONE")
        return "ERROR: DATA IS NONE"
    
    return request_handler.handle_put_item(company, data)

@app.route('/test/delete/{uuid}', methods=['DELETE'], cors=cors_config, authorizer=authorizer)
def delete_item(uuid):
    return request_handler.handle_delete_item(uuid)