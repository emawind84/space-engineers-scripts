#!/usr/bin/env python

import os
import sys
import logging
import json
import requests
import numpy as np
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

now = datetime.utcnow()

# friendly items name
fin = {
    "PreciseAutomaticRifleItem": "Precise Aut. Rifle",
    "UltimateAutomaticRifleItem": "Ultimate Aut. Rifle",
    "RapidFireAutomaticRifleItem": "Rapid Fire Aut. Rifle",
    "AutomaticRifleItem": "Automatic Rifle",
    "AngleGrinderItem": "Angle Grinder",
    "InteriorPlate": "Interior Plate",
    "LargeTube": "Large Steel Tube",
    "SmallTube": "Small Steel Tube",
    "MetalGrid": "Metal Grid",
    "HandDrillItem": "Hand Drill",
    "SolarCell": "Solar Cell",
    "Steel Plate": "Steel Plate",
    "BulletproofGlass": "Bulletproof Glass",
    "HydrogenBottle": "Hydrogen Bottle",
    "OxygenBottle": "Oxygen Bottle",
    "Medical": "Medical Comp.",
    "WelderItem": "Welder",
    "Thrust": "Thruster Comp.",
    "Reactor": "Reactor Comp.",
    "Construction": "Construction Comp.",
    "GravityGenerator": "Gravity Generator",
    "RadioCommunication": "Radio Communication",
    "PowerCell": "Power Cell"
}

plot_dir = 'plot'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

def create_plot(market):
    s = requests.session()

    with open('data-request-body.txt', 'r') as f:
        query = json.load(f)

    result = s.get('http://localhost:9200/_search', data=json.dumps(query))
    jresult = result.json()
    datalist = jresult['hits']['hits']

    items_quantity = []
    items_name = []
    for rowdata in datalist:
        item_type = rowdata['_source']['type']
        item_name = rowdata['_source']['item_name']
        if rowdata['_source']['market_name'] == market:
            _logger.debug(rowdata)
            items_quantity.append(rowdata['fields']['quantity.zerocap'][0])
            
            if item_type == "MyObjectBuilder_Ore":
                item_name += " Ore"
            elif item_type == "MyObjectBuilder_Ingot":
                item_name += " Ingot"
            items_name.append(fin.get(item_name, item_name))

    fig, ax = plt.subplots(figsize=(12,6))
    opacity = 0.4
    bar_width = 0.5
    n_groups = len(items_name)
    index = np.arange(n_groups)

    #ax.set_xlabel('Items')
    ax.set_ylabel('Quantity')
    ax.set_title('%s - Low Stock Items' % market)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(items_name)
    
    ax.text(0.98, 0.95, 'Updated on %s' % now.strftime('%Y-%m-%d %H:%M:%S UTC'),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='grey', fontsize=10)

    #plt.axhline(0, color='black', lw=2)

    # You can specify a rotation for the tick labels in degrees or with keywords.
    plt.xticks(rotation=45, ha='right')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.1)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)

    rects1 = ax.bar(index, items_quantity, bar_width,
                    alpha=opacity, color='r',
                    label='Items')

    fig.tight_layout()
    plt.savefig("%s/%s.png" % (plot_dir, market.lower().replace(' ', '-').replace('#', '-')), 
                bbox_inches = "tight",
                transparent=True, dpi=100)

def _main():
    market = sys.argv[1]
    
    #_logger.setLevel(logging.ERROR)

    create_plot(market)

if __name__=='__main__':   
    _main()