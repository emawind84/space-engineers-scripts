#!/usr/bin/env python

import sys
import json
import valve.source.a2s

def get_info(address='127.0.0.1', port=27016):
    SERVER_ADDRESS = (address, int(port))

    with valve.source.a2s.ServerQuerier(SERVER_ADDRESS, timeout=5) as server:
        info = server.info()

        infodict = {
            'player_count': info['player_count'],
            'version': info['version']
        }

        return(json.dumps(infodict))


if __name__=='__main__':
    address = sys.argv[1]
    port = sys.argv[2]
    print(get_info(address, port))