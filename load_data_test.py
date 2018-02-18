#!/usr/bin/env python

import sys
import logging
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

s = requests.session()

with open('data-request-body.txt', 'r') as f:
    query = json.load(f)

print(query)
result = s.get('http://localhost:9200/_search', data=json.dumps(query))
jresult = result.json()
datalist = jresult['hits']['hits']

items_quantity = []
items_name = []
for rowdata in datalist:
    if rowdata['_source']['market_name'] == 'Central Market':
        _logger.debug(rowdata)
        items_quantity.append(rowdata['_source']['quantity'])
        items_name.append(rowdata['_source']['item_name'])

fig, ax = plt.subplots(figsize=(12,6))
opacity = 0.4
bar_width = 0.35
n_groups = len(items_name)
index = np.arange(n_groups)

#ax.set_xlabel('Items')
ax.set_ylabel('Quantity')
ax.set_title('Missing Items')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(items_name)

plt.axhline(0, color='black', lw=2)

# You can specify a rotation for the tick labels in degrees or with keywords.
plt.xticks(rotation=45, ha='right')
# Pad margins so that markers don't get clipped by the axes
#plt.margins(0.1)
# Tweak spacing to prevent clipping of tick-labels
#plt.subplots_adjust(bottom=0.15)

rects1 = ax.bar(index, items_quantity, bar_width,
                alpha=opacity, color='b',
                label='Items')

fig.tight_layout()
plt.savefig("fig.png", 
            bbox_inches = "tight",
            transparent=True, dpi=100)
plt.show()