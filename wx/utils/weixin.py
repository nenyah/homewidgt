import logging

import requests

from homewidgt import settings

class WEIXINAPI:
    def __init__(self, appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET):
        self.appid = appid
        self.app_secret = app_secret
        self.root = 'https://api.weixin.qq.com/'

    def exchange_code_for_session_key(self, code):
        url = self.root + 'sns/jscode2session'
        params = {
            'appid': self.appid,
            'secret': self.app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        try:
            res = requests.get(url, params=params)

            if res.status_code == 200:
                return res
        except Exception as e:
            logging.error(f"连接失败,{e}")


if __name__ == '__main__':
    weixinapi = WEIXINAPI()
    session_info = weixinapi.exchange_code_for_session_key('061MLH00080AnM1DCv200I2SKN2MLH0U')
    print(session_info.text)
