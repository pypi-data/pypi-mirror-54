import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(npm_server, username, password)
    print("Custom Property Update Test:")
    results = swis.query(
        "SELECT Uri FROM Orion.Nodes WHERE NodeID=@id",
        id=1)  # set valid NodeID!
    uri = results['results'][0]['Uri']

    swis.update(uri + '/CustomProperties', City='Austin')
    obj = swis.read(uri + '/CustomProperties')
    print (obj)


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
