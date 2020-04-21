from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from Xtra.utils.response_code import RETCODE


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """自定义判断用户是否登陆的拓展类：返回JSON"""

    # 为什么只需要重写handle_no_permission？因为判断用户是否登陆的操作，父类已经完成
    # 子类只需要关心，如果用户未登录，对应怎样的操作
    def handle_no_permission(self):
        """直接响应JSON数据"""
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})