import json
import logging

from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from weixin import WXAPPAPI
from weixin.oauth2 import OAuth2AuthExchangeError

from .serializers import *

logger = logging.getLogger('django')


def create_or_update_user_info(openid, user_info):
    """
    创建或者更新用户信息
    :param openid: 微信 openid
    :param user_info: 微信用户信息
    :return: 返回用户对象
    """
    if openid:
        if user_info:
            user, created = WxUser.objects.update_or_create(openid=openid, defaults=user_info)
        else:
            user, created = WxUser.objects.get_or_create(openid=openid)
        return user
    return None


class WxLoginView(APIView):
    """
    post:
    微信登录接口
    """
    authentication_classes = []
    permission_classes = []
    fields = {
        'nick_name': 'nickName',
        'gender': 'gender',
        'language': 'language',
        'city': 'city',
        'province': 'province',
        'country': 'country',
        'avatar_url': 'avatarUrl',
    }

    def post(self, request):
        user_info = dict()
        code = request.data.get('code')
        logger.info("Code: {0}".format(code))
        user_info_raw = request.data.get('user_info', {})
        if isinstance(user_info_raw, str):
            user_info_raw = json.loads(user_info_raw)
        if not isinstance(user_info_raw, dict):
            user_info_raw = {}
        logger.info("user_info: {0}".format(user_info_raw))
        if code:
            api = WXAPPAPI(appid=settings.WX_APP_ID, app_secret=settings.WX_APP_SECRET)
            try:
                session_info = api.exchange_code_for_session_key(code=code)
            except OAuth2AuthExchangeError:
                session_info = None
            if session_info:
                openid = session_info.get('openid', None)
                if openid:
                    if user_info_raw:
                        for k, v in self.fields.items():
                            user_info[k] = user_info_raw.get(v)
                    user = create_or_update_user_info(openid, user_info)
                    if user:
                        token = JfwTokenObtainPairSerializer.get_token(user).access_token
                        return Response(
                            {
                                'jwt': str(token),
                                'user': model_to_dict(
                                    user,
                                    fields=[
                                        'company', 'restaurant', 'current_role',
                                        'is_owner', 'is_client', 'is_manager'
                                    ])
                            },
                            status=HTTP_200_OK)
        return Response({'jwt': None, 'user': {}}, status=HTTP_204_NO_CONTENT)
