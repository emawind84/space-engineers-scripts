#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import es_data_import as ES
from datetime import datetime

__author__ = "Emanuele Disco"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "emanuele.disco@gmail.com"
__status__ = "Production"

def fix_encoding(filepath='EconomyData.xml'):
    content = '<?xml version="1.0" encoding="utf-8"?>\n'
    with open(filepath, 'r') as f:
        f.readline()
        for line in f:
            content += line
    with open(filepath, 'w') as f:
        f.write(content)

def import_data(filepath='EconomyData.xml'):
    now = datetime.utcnow()
    index_suffix = now.strftime('%Y.%m.%d')
    tree = ET.parse(filepath)
    root = tree.getroot()

    #for child in root:
    #    print(child)

    for pl in root.iter('ClientAccount'):
        bal = pl.find('BankBalance')
        name = pl.find('NickName')
        data = { 
            'name': name.text, 
            'balance': bal.text,
            'timestamp': now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }
        ES.post(data=data, index='se-user-balance-' + index_suffix, typez='doc')

    for pl in root.iter('Market'):
        market_name = pl.find('DisplayName').text

        for item in pl.iter('MarketItem'):
            blacklisted = item.find('IsBlacklisted').text
            if blacklisted == 'true':
                continue

            data = {
                'market_name': market_name,
                'type': item.find('TypeId').text,
                'item_name': item.find('SubtypeName').text, 
                'quantity': item.find('Quantity').text,
                'sellprice': item.find('SellPrice').text,
                'buyprice': item.find('BuyPrice').text,
                'timestamp': now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            }
            ES.post(data=data, index='se-market-item-' + index_suffix, typez='doc')
            
def _main():
    filepath = sys.argv[1]

    fix_encoding(filepath)
    import_data(filepath)

if __name__=='__main__':   
    _main()