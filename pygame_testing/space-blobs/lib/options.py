import json
import sys
import os

def generate_settings(options):

    settings = {}


    settings = options

    if len(sys.argv) > 1:
        for key in options.keys():
            if key in sys.argv:
                print('{0} found'.format(key))
                pos = sys.argv.index(key)
                print('key positions {0}'.format(pos))
                value = None
                if type(options[key]) is not bool:
                    print('key not bool {0} {1} {2}'.format(key, options[key], type(options[key])))
                    value = sys.argv[pos + 1]
                if value == None:
                    settings[key] = True
                else:
                    if str(value) in [str(o) for o in options[key]]:
                        settings[key] = str(value)
                    else:
                        print('value {0} is invalid for setting {1}'.format(value, key))
                        
        with open('settings.json', 'w') as sf:
            sf.write(json.dumps(settings))
            
                
    else:
        files = os.listdir('.')
        if 'settings.json' in files:
            with open('settings.json', 'r') as sf:
                settings = json.loads(sf.read())
                for ok in options.keys():
                    if ok not in settings.keys():
                        if type(options[ok]) is not bool:
                            settings[ok]=options[ok][0]
                        else:
                            settings[ok]=options[ok]

    return settings