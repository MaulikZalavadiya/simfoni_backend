from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import requests
import json
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


# def demo():
#     print(">>>>>>>>>>>")

class ListRepo(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def post(self, request, format=None):
        # demo()
        """
        Return a list of all users.
        """
        # type = request.data.get('type')
        # search = request.data.get('search')
        type = request.query_params.get('type')
        search = request.query_params.get('search')
        page = request.query_params.get('page',1)
        j_st = json.dumps({"type":type,"search":search,"page":page})
        try:
            tmp_ls = json.loads(redis_instance.get(j_st))
            print("from caches")
            return Response(data=tmp_ls)
        except:
            pass
        if type=='repositories':
            headers = {'Authorization':'Bearer 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','Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version':'2022-11-28'}
            resp = requests.get(f'https://api.github.com/search/repositories?q={search}&page={page}', headers=headers)
            resp = json.loads(resp.text)
            tmp_ls= []
            for i in resp['items']:
                tmp_dict = {}
                tmp_dict['username'] = i['owner']['login']
                tmp_dict['profile'] = i['owner']['avatar_url']
                tmp_dict['repo_url'] = i['owner']['url']
                tmp_dict['stargazers_count'] = i['stargazers_count']
                tmp_dict['full_name'] = i['full_name']
                tmp_ls.append(tmp_dict)
            print(tmp_ls)
            print("from data")
            redis_instance.set(j_st, json.dumps(tmp_ls))
            return Response(data=tmp_ls)
        elif type=='user':
            headers = {'Authorization':'Bearer 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','Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version':'2022-11-28'}
            resp = requests.get(f'https://api.github.com/search/users?q={search}&page={page}', headers=headers)
            resp = json.loads(resp.text)
            tmp_ls= []
            for i in resp['items']:
                tmp_dict = {}
                tmp_dict['username'] = i['login']
                tmp_dict['profile'] = i['avatar_url']
                tmp_dict['repo_url'] = i['url']
                tmp_ls.append(tmp_dict)
            redis_instance.set(j_st, json.dumps(tmp_ls))
            return Response(data=tmp_ls)
        elif type =='issues':
            headers = {'Authorization':'Bearer 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','Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version':'2022-11-28'}
            resp = requests.get(f'https://api.github.com/search/issues?q={search}&page={page}', headers=headers)
            resp = json.loads(resp.text)
            tmp_ls= []
            for i in resp['items']:
                tmp_dict = {}
                tmp_dict['username'] = i['user']['login']
                tmp_dict['profile'] = i['user']['avatar_url']
                tmp_dict['repo_url'] = i['url']
                tmp_ls.append(tmp_dict)
            redis_instance.set(j_st, json.dumps(tmp_ls))
            return Response(data=tmp_ls)

# @as_view(['GET'])
class ClearCatch(APIView):
    def post(self, request, format=None):
        k = redis_instance.keys()
        if len(k) > 0:
            redis_instance.delete(*k)
        return Response(data={"ok":"ok"})