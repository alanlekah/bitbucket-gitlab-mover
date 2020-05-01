import json
import requests
import base64
import argparse
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bitbucket_server_url', type=str, help='The bitbucket server URL')
    parser.add_argument('bitbucket_project', type=str, help='The bitbucket project to move')
    parser.add_argument('personal_access_token', type=str, help='Personal access token')
    parser.add_argument('to_url', type=str, help='The gitlab subgroup or group where you want the repos to be placed.'
                                                 ' For example, should be your cloning url '
                                                 'git@gitlab.example.com:namespace/')
    #parser.add_argument('username', type=str, help='username to login to bitbucket server')
    #parser.add_argument('password', type=str, help='password to login to bitbucket server')
    return parser.parse_args()


args = parse_args()

bitbucket_server_url = args.bitbucket_server_url
bitbucket_project = args.bitbucket_project
#username = args.username
#password = args.password
personal_access_token = args.personal_access_token
to_url = args.to_url


bitbucket_base_url = f"{bitbucket_server_url}/rest/api/1.0/projects/{bitbucket_project}/repos"

#userpass = f"{username}:{password}"
#encoded = base64.encodebytes(userpass.encode('utf-8'))
#str_encoded = encoded.decode('utf-8').strip()

auth_headers = {'Authorization': f'Bearer {personal_access_token}',
                'Content-Type': 'application/json'}

response = requests.get(bitbucket_base_url, headers=auth_headers)

js = json.loads(response.content.decode('utf-8'))

# Loop through each repo in the block
for value in js['values'][2:]:
    new_base_url = f"{bitbucket_base_url}/{value['name']}"
    new_response = requests.get(new_base_url, headers=auth_headers)

    # get each individual pages ssh clone url
    new_js = json.loads(new_response.content.decode('utf-8'))

    for clone_url in new_js['links']['clone']:
        if clone_url['name'] == 'ssh':
            ssh_clone_url = clone_url['href']

            subprocess.run(f"git clone --mirror {ssh_clone_url} && cd {value['name']}.git && git remote set-url --push origin"
                           f" {to_url}/{value['name']}.git && git push --set-upstream {to_url}/{value['name']}.git --mirror",
                           shell=True, check=True)






