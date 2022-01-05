import json
import requests
import pandas as pd
import urllib.request
from time import sleep
import os
import sys
import argparse

def obtain_image(api, folder, card):
    r = requests.get(api+card).json()
    link = r['data'][0]['image_uris']['png']
    name = r['data'][0]['name']
    cardfilename = card.replace(' ','_')+'.png'
    save = urllib.request.urlretrieve(link, os.path.join(folder,cardfilename))
    sleep(0.2)
    return folder+cardfilename, name

def nandeck_code(filewithcard,totalcard):
    s="LINKMULTI = quantity\n\
LINK = "+filewithcard+"\n\
[range] = "+"\"1-"+str(totalcard)+'\"'+"\n\
CARDS="+str(totalcard)+"\n\
CARDSIZE = 6.3, 8.8\n\
DPI=300\n\
IMAGEFILTER = LANCZOS\n\
OVERSAMPLE = 2\n\
FONTALIAS = [range], ON\n\
image=[range],[image],0,0,6.3, 8.8,0,N\n\
BORDER=RECTANGLE"
    fileout = filewithcard[:-5]+'.txt'
    with open(fileout, "w") as text_file:
        text_file.write(s)
    return fileout
        
        
def print_cards(filewithcard,totcard):
    search = 'https://api.scryfall.com/cards/search?q='
    df = pd.read_excel(filewithcard)
    cards = list(df.name)
    totcard = sum(df.quantity)

    fileout = nandeck_code(filewithcard,totcard)


    list_images = []
    errors = []
    errors_download = []
    for card in cards:
        card = card.strip()
        try:
            link, nome = obtain_image(search,'',card)
        except KeyError:
            print('I cannot find this card: {}.'.format(card))
            list_images.append('')
            errors.append(card)
            errors_download.append('not_found')
            continue
        list_images.append(link)
        if card.lower()!=nome.lower():
            errors.append(card)
            errors_download.append(nome)
        
    df['image'] = list_images

    df.to_excel(filewithcard, index=False)

    command = "wine nandeck \""+fileout+"\" /createpdf"
    os.system(command)

    if len(errors)==0:
        print('Finish. Ok.')
    else:
        print('Are these cards wrong?')
        for card, down in zip(errors, errors_download):
            print('Request: {}. Found: {}'.format(card, down))
        print('Please manually control generated .xlsx.')
    return
        
        
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    
    parser.add_argument('-e', '--excel', help='Excel file with cards', required=False, default='cards.xlsx')
    parser.add_argument('-f', '--folder', help='Folder', required=False, default='')
    parser.add_argument('-n', '--number', help='Total card to create', required=False, default=9)

    args = parser.parse_args()
    
    
    print_cards(args.excel, args.number)
    
