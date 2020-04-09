from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django import http

from . import constants
from Xtra.utils.response_code import RETCODE
from verifications.lib.captcha.captcha import captcha


class CheckImageCodeView(View):
    """短信验证码"""

    def get(self, request):
        """

        :param request:
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 创建连接道redis的对象
        redis_conn = get_redis_connection('verify_code')

        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已失效'})

        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        # 将bytes转字符串，再比较
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():      # 转小写，再比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '输入图形验证码正确'})


# Create your views here.
class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """

        :param request:
        :param uuid: 通用唯一识别码，用于唯一标识该图形验证码属于哪个用户的
        :return: image/jpg
        """
        # 接收和校验参数(uuid)
        # 实现主体业务逻辑（生成-保存-响应 图形验证码）
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        # redis_conn.setex('key', 'expires', 'value')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 响应图形验证码
        # return http.HttpResponse('响应体', '数据类型')
        return http.HttpResponse(image, content_type='image/jpg')