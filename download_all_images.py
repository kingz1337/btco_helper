#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import wget
import os
import time
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

meme_images = ['https://images.dontbuymeme.com/collections/bitcoin-origins/mp4/wheel-of-fortune.mp4',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/inception.jpg',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/proliferation.jpg',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/propagation.jpg',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/the-affirmation-seed.jpg',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/pizza-day.jpg',
               'https://images.dontbuymeme.com/collections/bitcoin-origins/static/pride-of-the-lotus.jpg',
              ]

def main():

    # get all images from the meme pool
    if not os.path.exists("meme_pool"):
        os.makedirs("meme_pool")
    for i in meme_images:
        meme_path = "meme_pool"+os.path.sep+i.split('/')[-1]
        if not os.path.isfile(meme_path):
            try:
                wget.download(i, out=meme_path)
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
                print("Oops we hit an error - " + e + "\n")
                print("Don't worry we're going to try again in 5 seconds\n")
                time.sleep(5)
                wget.download(i, out=meme_path)
            except Exception as e:
                print("Oops we really hit an error - " + e + "\n")
                print("Don't worry we're going to try again in 10 seconds\n")
                time.sleep(10)
                wget.download(i, out=meme_path)

    # get the number of templates on atomichub
    r = requests.get('https://wax.api.atomicassets.io/atomicassets/v1/collections/bitcoinorign/stats')
    tmp = r.json()
    num_templates = int(tmp['data']['templates'])
    # get all templates
    r = requests.get('https://wax.api.atomicassets.io/atomicassets/v1/templates?limit='+str(num_templates)+'&page=1&collection_name=bitcoinorign')
    templates = r.json()
    for i in range(int(num_templates)):
        img = templates['data'][i]['immutable_data']['img']
        back_img = templates['data'][i]['immutable_data']['backimg'] if 'backimg' in templates['data'][i]['immutable_data'] else None
        name = templates['data'][i]['name']
        moment = templates['data'][i]['immutable_data']['moment'] if 'moment' in templates['data'][i]['immutable_data'] else None
        rarity = templates['data'][i]['immutable_data']['rarity'] if 'rarity' in templates['data'][i]['immutable_data'] else None

        folder = 'moment '+moment if moment is not None else 'other'
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename_1 = name+'_'+rarity if rarity is not None else name
        filename_2 = filename_1+'_'+'backimage' if back_img is not None else None
        filetype_1 = requests.head("https://ipfs.io/ipfs/"+img)
        filetype_1 = filetype_1.headers['Content-Type'].split('/')[-1]

        if filename_2 is not None:
            filetype_2 = requests.head("https://ipfs.io/ipfs/"+back_img)
            filetype_2 = filetype_2.headers['Content-Type'].split('/')[-1]

        path_1 = folder+os.path.sep+filename_1+'.'+filetype_1
        if not os.path.isfile(path_1):
            try:
                wget.download("https://ipfs.io/ipfs/"+img, out=path_1)
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
                print("Oops we hit an error - " + e + "\n")
                print("Don't worry we're going to try again in 5 seconds\n")
                time.sleep(5)
                wget.download("https://ipfs.io/ipfs/"+img, out=path_1)
            except Exception as e:
                print("Oops we really hit an error - " + e + "\n")
                print("Don't worry we're going to try again in 10 seconds\n")
                time.sleep(10)
                wget.download("https://ipfs.io/ipfs/"+img, out=path_1)

        if back_img is not None:
            path_2 = folder+os.path.sep+filename_2+'.'+filetype_2
            if not os.path.isfile(path_2):
                try:
                    wget.download("https://ipfs.io/ipfs/"+back_img, out=path_2)
                except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
                    print("Oops we hit an error - " + e + "\n")
                    print("Don't worry we're going to try again in 5 seconds =)")
                    time.sleep(5)
                    wget.download("https://ipfs.io/ipfs/"+back_img, out=path_2)
                except Exception as e:
                    print("Oops we really hit an error - " + e + "\n")
                    print("Don't worry we're going to try again in 10 seconds =)")
                    time.sleep(10)
                    wget.download("https://ipfs.io/ipfs/"+back_img, out=path_2)

    print("\nFinished")

if __name__ == "__main__":
    # execute only if run as a script
    main()
