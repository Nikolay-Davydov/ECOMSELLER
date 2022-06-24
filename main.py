import ozone_seller
import configparser


def load_config():
    conf = configparser.ConfigParser()
    conf.read('conf.ini')
    id = conf.get('default', 'ID')
    key = conf.get('default', 'KEY')
    url = conf.get('default', 'URL')
    version = conf.get('default', 'VERSION')
    return {'id': id, 'key': key, 'url': url, 'version': version}


config = load_config()
seller = ozone_seller.OzoneSeller(config)
all_actions = seller.get_actions()
products_for_actions = {}
for action in all_actions:
    products_for_action = seller.get_candidates(action['id'])
    products_for_actions[action['id']] = {'products': products_for_action, 'info': action}

print(products_for_actions)


