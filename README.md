# Usage

The program has four parameters:

- `bitbucket_server_url`: the bitbucket server url
- `bitbucket_project`: the project name you wish to move
- `personal_access_token`: the bitbucket personal access token (can be created under account, only needs read access)
- `to_url`: the ssh url of the subgroup in gitlab you wish to push to. i.e: git@gitlab.example.com:namespace/subgroup/

Command: `python3 bitbucket-clone-pusher.py <bitbucket_server_url> <bitbucket_project> <access_token> <to_url>`