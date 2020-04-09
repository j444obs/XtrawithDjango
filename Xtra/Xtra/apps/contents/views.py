from django.shortcuts import render
from django.views import View

# Create your views here.


class IndexView(View):

    def get(self, request):
        """
        展示首页
        :param request:
        :return:
        """
        return render(request, "index.html")


class BackupView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass