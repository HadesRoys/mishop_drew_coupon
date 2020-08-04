import requests

http_session = requests.Session()

def qywx_pusher(content):
    """
    @param content:
    @return:
    """
    params = {
        "uid": 'uid_8ea094e9c33a306bf36ff40b6977032f8a7270a86712c90dd12047eb506f4ee8',
        "content": content,
    }
    resp = http_session.get('http://qywxapi.hadesroys.com/api/push/message', params=params, timeout=2)
    if resp.status_code == 200:
        return True
    return False

if __name__ == '__main__':
    print(qywx_pusher("1"))
