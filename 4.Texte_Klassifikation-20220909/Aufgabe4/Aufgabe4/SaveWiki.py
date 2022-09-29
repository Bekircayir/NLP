import requests
import codecs
import os

def savePage(title,folder):
    
    response = requests.get(
    'https://de.wikipedia.org/w/api.php',
    params={
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'explaintext': True
        }
    ).json()
    
    text = ''
    pagelist = response.get('query').get('pages')
    for page in pagelist:
        wikipage = pagelist[page]
        text = wikipage['extract']
        break
    
    if not os.path.isdir(folder):
        os.mkdir(folder)
    f = codecs.open(folder+'/'+title.replace(' ','_')+'.txt','w','utf8')
    f.write(text)
    f.close()
    return
   

def getWikiPages(category):
    titles = []
    response = requests.get(
        'https://de.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': 'Category:'+category,
            'cmtype':'page',
            'format': 'json'
        }
    ).json()


    while(response):
        titles.extend( [t['title'] for t in response['query']['categorymembers']] )
        if 'continue' in response:
            cont = response['continue']['cmcontinue']
            response = requests.get(
                'https://de.wikipedia.org/w/api.php',
                params={
                    'action': 'query',
                    'list': 'categorymembers',
                    'cmtitle': 'Category:' + category,
                    'cmtype': 'page',
                    'cmcontinue': cont,
                    'format': 'json'
                }
            ).json()
        else:
            break

        if not cont:
            response = None

    return titles


def downloadWikiCat(category,folder,recursive=False):
    titles = getWikiPages(category)
    for t in titles:
        if r'/' not in t:
           savePage(t,folder)
    return