from flask import Flask
import json
import re
import requests
import sys
import yaml

app = Flask(__name__)
__argument__ = None


@app.route('/v1/<string:path>', methods=['GET'])
def hello(path):
    if __argument__ == '--help':
        return 'Provide the git repo path'
    else:
        url = __argument__
        regex = r"https://github.com/([^/].*)/([^/].*)"
        (user, repo) = re.match(regex, url).groups()
        response = requests.get('https://api.github.com/repos/' + user
                                + '/' + repo + '/contents/' + path)
        if response:
            data = json.loads(response.text)
            content = data['content'].decode('base64')
            if '.yml' in data['name']:
                welcome_message = \
                    yaml.load(content).get('welcome_message', None)
                yaml_response = {}
                yaml_response['welcome_message'] = welcome_message
                if welcome_message:
                    return yaml.dump(yaml_response)
                else:
                    return 'No welcome_message in the config'
            elif '.json' in data['name']:
                welcome_message = \
                    json.loads(content).get('welcome_message', None)
                json_response = {}
                json_response['welcome_message'] = welcome_message
                if welcome_message:
                    return json.dumps(json_response, indent=4,
                            separators=(',', ': '))
                else:
                    return 'No welcome_message in the config'
            else:
                return 'Not supported config format, please use yml or json'
        else:

            return 'Error in fetcting from repo:' + response.text

if __name__ == '__main__':
    if len(sys.argv):
        __argument__ = sys.argv[1]
        app.run(debug=True, host='0.0.0.0')

			