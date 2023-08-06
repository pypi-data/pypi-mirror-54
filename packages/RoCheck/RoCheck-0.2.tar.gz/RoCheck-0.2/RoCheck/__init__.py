import json
import requests


class auth:
    def __init__(self, cookie, link='https://assetgame.roblox.com/Game/PlaceLauncher.ashx?request=RequestGameJob'
                                    '&placeId={}&gameId={}'):
        self.request = None
        self.cookie = cookie
        self.link = link

    def roblox_request(self, link, place_id):
        cookie = {
            '.ROBLOSECURITY': self.cookie,
            'path': '/',
            'domain': '.roblox.com'
        }

        cookie['.ROBLOSECURITY'] = cookie['.ROBLOSECURITY'].replace('\\n', '')

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Referer': "https://www.roblox.com/games/" + place_id,
            'Origin': 'https://www.roblox.com'
        }

        request = requests.get(link, cookies=cookie, headers=headers)
        return request

    def get_ip(self, place_id, job_id):
        link = self.link.format(str(place_id), str(job_id))

        request = self.roblox_request(link, place_id)

        if request.status_code == 403:
            raise ValueError("Cookie is not valid")
        else:
            pass

        ip_request = requests.get(json.loads(request.text)['joinScriptUrl'])

        return json.loads('\n'.join(ip_request.text.split('\n')[1:]))['MachineAddress']

    def verify_ip(self, place_id, ip):
        request = self.roblox_request(
            f'https://games.roblox.com/v1/games/{place_id}/servers/Public?sortOrder=Asc&limit=100', place_id).text

        request = json.loads(request)

        verified = False
        for data in request['data']:
            ip_verify = self.get_ip(place_id, data['id'])
            if ip_verify == ip:
                verified = True
                break

        return verified
