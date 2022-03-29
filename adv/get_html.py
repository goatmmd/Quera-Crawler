import requests

def get(link, *args):
    try:
        response = requests.get(link)
    except requests.HTTPError as e:
        print(e)
        return None
    print(response.url)
    return response.text
