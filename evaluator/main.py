import json

import requests

from resolve import resolve
from jsonfind import find_and_modify

if __name__ == '__main__':
    response = requests.get('http://localhost:5000')
    body = response.json()
    print(f'response body: {json.dumps(body["container"]["params"], indent=4)}')
    for resolver in body['resolvers']:
        value = resolve(resolver, resolver['target']['type'])
        find_and_modify(resolver['target']['query'], body['container']['params'], value)

    print(f'resolved body: {json.dumps(body["container"]["params"], indent=4)}')

