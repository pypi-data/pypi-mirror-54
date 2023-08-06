import json,requests,sys,os,hcl

class TFCloud:
    api_base_url = 'https://app.terraform.io/api/v2'

    def __init__(self):
        self.api_token = self.get_api_token()

    def _get_from_api(self, url):
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            sys.exit('Error calling: {}, {}'.format(url, response))


    def _get_headers(self):
        return {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {0}'.format(self.api_token)
        }

    def get_workspace_id(self, organization_name, workspace_name):
        url = "{}/organizations/{}/workspaces/{}".format(self.api_base_url,organization_name, workspace_name)
        workspace = self._get_from_api(url)
        return workspace['data']['id']

    def get_current_state(self, workspace_id):
        url = "{}/workspaces/{}/current-state-version?include=outputs".format(self.api_base_url,workspace_id)
        state = self._get_from_api(url)
        return state

    def get_current_state_outputs(self, worspace_id):
        state = self.get_current_state(worspace_id)

        included_outputs = filter(lambda included: included['type'] == 'state-version-outputs', state['included'])

        outputs = {}
        for output in included_outputs:
            outputs[output['attributes']['name']] = output['attributes']['value']

        return outputs

    def get_api_token(self):
        if 'TF_CLOUD_ACCESS_KEY' in os.environ:
            return os.environ['TF_CLOUD_ACCESS_KEY']

        home_path = os.environ['HOME']
        try:
            credentials_file = self.read_hcl_file('{}/.terraformrc'.format(home_path))
            return credentials_file['credentials']['app.terraform.io']['token']
        except FileNotFoundError:
            sys.exit('Missing valid credentials file in {}/.terraformrc'.format(home_path))
        except ValueError:
            sys.exit('Invalid credentials file format')

    def read_hcl_file(self,filename):
        with open(filename, 'r') as fp:
            return hcl.load(fp)
