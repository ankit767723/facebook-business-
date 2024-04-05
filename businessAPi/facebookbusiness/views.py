import facebook
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests

def facebook_login(request):
    # Generate a login URL
    oauth_url = 'https://www.facebook.com/dialog/oauth'
    redirect_uri = 'http://localhost:8000/facebook/business/'
    scope = 'public_profile,manage_pages,publish_to_groups,ads_management'
    oauth_url += '?client_id={}&redirect_uri={}&scope={}'.format('3609238529329762', redirect_uri, scope)

    return HttpResponseRedirect(oauth_url)

def facebook_business(request):
    if 'code' not in request.GET:
        return facebook_login(request)

    # Exchange the code for an access token
    oauth_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'http://localhost:8000/facebook/business/'
    app_id = '3609238529329762'
    app_secret = '59189b648f1040f5e64a982e5be26ca9'
    code = request.GET['code']
    oauth_url += '?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(app_id, redirect_uri, app_secret, code)

    response = requests.get(oauth_url)
    access_token = response.json()['access_token']

    # Use the access token to call Facebook Business APIs
    graph = facebook.GraphAPI(access_token=access_token)
    pages = graph.get_connections('me', 'accounts')

    return render(request, 'facebook_business.html', {'pages': pages})