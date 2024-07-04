from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def getsongdata(text):
    # url = "https://jiosaavanapi-rouge.vercel.app/api/search/songs"
    url = "https://saavn.dev/api/search/songs"
    querystring = {"query":text}
    response = requests.get(url, params=querystring)
    data= response.json()
    return data

def extract_song_details(data):
            song_name = data['data']['results'][0]['name']
            song_artistss = [artist['name'] for artist in data['data']['results'][0]['artists']['primary']]
            song_artists = song_artistss[0]
            image_url = next(image["url"] for song in data["data"]["results"] for image in song["image"] if image["quality"] == "500x500")
            song_url_320kbps = next((item['url'] for item in data['data']['results'][0]['downloadUrl'] if item['quality'] == '320kbps'), None)
            return {'songname':song_name, 'artist':song_artists, 'songurl':song_url_320kbps, 'imgurl':image_url}

# Create your views here.
def home(request):
    if request.method == 'POST':
        song_name = request.POST.get("songname")
        data = getsongdata(song_name)
        pdata = extract_song_details(data)
        return render(request, 'final.html', pdata)
    return render(request, 'home.html')


def record(request):
    return render(request, 'record.html')

@csrf_exempt
def save_speech_text(request):
    global spoken_text
    if request.method == 'POST':
        spoken_text = request.POST.get('text')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

# def display_text(request):
#     global spoken_text
#     data = getsongdata(spoken_text)
#     pdata = extract_song_details(data)
#     return render(request, 'final.html', pdata)

from django.http import HttpRequest
from .decorators import internal_only


def display_text(request):
    global spoken_text
    data = getsongdata(spoken_text)
    pdata = extract_song_details(data)
    return render(request, 'final.html', pdata)

def custom_404(request, exception):
    return render(request, '404.html', status=404)