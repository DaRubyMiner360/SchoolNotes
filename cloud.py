import json
import sys
import urllib.request


def log(text):
    with open("cloud.log", "a+") as f:
        f.write(str(text))
        f.write("\n")

if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)
            
    context, book = json.load(sys.stdin)
    
    log(book)

    variables = {
        'docs_version': '0.0.1'
    }

    url = 'https://meta.cloudmc.ml/v2/versions/loader/'
    try:
        urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    except:
        url = 'https://cloudmc.ml/files/promotions_slim.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        if 'meta.' in url:
            # TODO: Adjust to API
            variables['version'] = data[0]['latest']['version']
        else:
            variables['version'] = data['promos']['latest']

    if variables['version'] == variables['docs_version']:
        variables['version_text'] = 'The current version is ' + variables['version'] + '.'
    else:
        variables['version_text'] = 'Warning: This documentation is for ' + variables['docs_version'] + ' but the latest version is ' + variables['version'] + '. Some things might have changed since the docs were last updated.'
    
    log(variables)
    
    for i in range(len(book['sections'])):
        for key in variables:
            if 'Chapter' in book['sections'][i]:
                book['sections'][i]['Chapter']['content'] = book['sections'][i]['Chapter']['content'].replace('{{ ' + key + ' }}', variables[key])
            
    print(json.dumps(book))
