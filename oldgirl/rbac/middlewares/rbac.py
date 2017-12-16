import re

from django.shortcuts import redirect,HttpResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request):
        permission_url_dic=request.session.get("permission_dic")
        current_url= request.path
        for url in settings.WHITE_LIST:
            if re.match(url,current_url):
                return None

        for group_id,url_code in permission_url_dic.items():
            for url in url_code["urls"]:
                regex="^{0}$".format(url)
                if re.match(regex,current_url):
                    request.permission_codes=url_code["codes"]
                    menu_list = request.session["menulist"]



                    return None
                else:
                    return HttpResponse("无权访问")
