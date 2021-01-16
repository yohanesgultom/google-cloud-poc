import flask
import json
import requests

service_name = 'alpha'

app = flask.Flask(__name__)


@app.route('/')
def index():
    headers = json.dumps(flask.request.headers, default=str)
    return {
        'message': f'this is {service_name} service',
        'headers': headers,
    }


@app.route('/trailing-slash/')
def trailing_slash():
    """
    Path with trailing slash
    :return:
    """
    headers = json.dumps(flask.request.headers, default=str)
    return {
        'message': f'this is {service_name} trailing-slash service',
        'headers': headers,
    }


@app.route('/action', methods=['POST',])
def action():
    """
    Simulates a proxy by making a HTTP request to given URL
    :return:
    """
    body = flask.request.json
    headers = json.dumps(flask.request.headers, default=str)
    url = body['url']
    r = requests.get(url)
    return {
        'headers': headers,
        'message': f'{service_name} action success', 
        'url': url, 
        'response': r.json(),
    }


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)