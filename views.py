from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse

from .utilities.detection import VideoCamera
# from yogguru.pushups import RepsVideoCamera

from django.views.decorators import gzip
from django.views.decorators.http import condition
import random, cv2



def index(req):
    return render(req, 'basic/index.html')

def header(req):
    return render(req, 'basic/header.html')
    
def profile(req):
    return render(req, 'basic/profile.html')




# YOGA PRACTICE
yp = ''
def yogaprac(req, yogapose):
    print(yogapose)
    global yp
    yp = yogapose
    return render(req, 'practice/camera.html', {'pose': yogapose})
def closePractice(req):
    camera.__del__()
    global isCamera
    isCamera = False
    return HttpResponse('closed')

camera = ''
isCamera = False
def gen():
    k = 0
    while camera.status:
        print('gen -> ', k)
        camera.poseName = yp
        frame = camera.get_frame()
        # print('frame ', frame)
        if frame:
            # k += 1
            print('frame ', frame)
            img_url = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            return img_url
def txt():
    while True:
        if isCamera:
            print(camera.trainer_text)
            return camera.trainer_text+"..."
            if not camera.status:
                break
        else:
            return "Open the camera..."
            # return "Opening the camera..."

@gzip.gzip_page
def video_feed(req, type):
    print('vf -> ', yp)
    print(type)
    global camera
    # if type == 'prac':
    camera = VideoCamera()
    # camera = cv2.VideoCapture(0)
    # else:
    #     camera = RepsVideoCamera()
    global isCamera
    isCamera = True
    response = StreamingHttpResponse(gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    response['Cache-Control'] = 'no-cache'
    return response

def msg_feed(req, type):
    print('msg -> ', yp)
    response = StreamingHttpResponse(txt(), content_type='text/html')
    response['Cache-Control'] = 'no-cache'
    return response





# MULTI PLAYER GAME
def game(req):
    return render(req, 'game/gameDashboard.html')

def room_view(request, roomId):
    print(roomId)
    user_name = request.session['user_name']
    print(user_name)
    isHost = request.session['isHost']
    del request.session['isHost']
    del request.session['user_name']
    return render(request,'game/room.html',{
        'user_name' : user_name,
        'roomId' : roomId,
        'isHost' : isHost
    })

def createRoom(request,user_name):
    print(user_name)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    size = 8
    roomId = ''.join(random.choice(chars) for x in range(size))
    print(roomId)
    request.session['user_name'] = user_name
    request.session['isHost'] = 'yes'
    return redirect('/room/'+roomId)

def joinRoom(request, user_name, roomId):
    print(user_name)
    print(roomId)
    request.session['user_name'] = user_name
    request.session['isHost'] = 'no'
    return redirect('/room/'+roomId)



def notFound(req):
    return render(req, 'basic/upcoming_page.html')