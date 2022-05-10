import math

from numpy.lib.function_base import select
import cv2
import numpy as np
import time
import mediapipe as mp
import matplotlib.pyplot as plt
from .classification import *
# from yogguru.suryaNam import Surya_Namaskar_Classification


mp_pose = mp.solutions.pose # Initializing mediapipe pose class.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils # Initializing mediapipe drawing class, useful for annotation.

class Detection:
    def detectPose(image, pose): # pose: The pose setup function required to perform the pose detection.
        output_image = image.copy()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(imageRGB)
        height, width, _ = image.shape
        landmarks = []
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS)
            for landmark in results.pose_landmarks.landmark:
                landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                    (landmark.z * width)))
        return output_image, landmarks


class HelperFunction:
    def initFunc(landmarks, curr_pose, curr_side):
        angles = {}
        angles['left_elbow_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        angles['right_elbow_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
        angles['left_shoulder_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
        angles['right_shoulder_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
        angles['left_knee_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
        angles['right_knee_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        angles['left_hip_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
        angles['right_hip_angle'] = HelperFunction.calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

        posefuncs = {
            'tree_pose': Classification1.classifyTreePose(angles, landmarks),
            'warrior1_pose': Classification1.classifyWarrior1Pose(curr_side, angles, landmarks),
            'warrior2_pose': Classification1.classifyWarrior2Pose(curr_side, angles, landmarks),
            'triangle_pose': Classification1.classifyTrianglePose(curr_side, angles, landmarks),
            'bridge_pose': Classification1.classifyBridgePose(angles, landmarks),
        }
        return posefuncs[curr_pose]        
    def calculateAngle(landmark1, landmark2, landmark3):
        x1, y1, _ = landmark1
        x2, y2, _ = landmark2
        x3, y3, _ = landmark3
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        return angle


class VideoCamera(object):
    pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
    poseName = ''
    side = 'R'
    ishold = False
    isOver = False
    isSideChange = False
    firstInstance = 0
    def __init__(self):
        print('cam')
        self.video = cv2.VideoCapture(0)
        self.status = True
        self.trainer_text = 'Opening the camera'
        self.surya_nam_curr_pose = 1

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        self.status = False

    def get_frame(self):
        print('get frame', self.poseName)
        ok, frame = self.video.read()
        print(ok)
        frame = cv2.flip(frame, 1)
        msg = ''
        if not ok:  
            print('not ok')  
            return ''

        frame, landmarks = Detection.detectPose(frame, self.pose_video)

        print('labdmarks')
        if landmarks and not self.ishold and not self.isOver:   
            if self.isSideChange:
                self.isSideChange = False
                self.startTimer(3) 
            msg = HelperFunction.initFunc(landmarks, self.poseName, self.side)
        if self.ishold:
            self.startTimer(5)
            self.ishold = False
            if self.side == 'R':
                self.ishold = False
                print('self side')
                self.side = 'L'
                self.isSideChange = True
                msg = "Now, left side"
            else:
                self.ishold = False
                print('over')
                msg = 'Over!'
                self.isOver = True
        if self.isOver:
            msg = 'Over!'
        if not landmarks:
            msg = 'Please wait! we are detecting your movements'

        _, jpeg = cv2.imencode('.jpg', frame)
        # print(msg)
        if msg != '':
            if msg == 'success':
                msg = 'Hold in the same position'
                self.ishold = True
            self.trainer_text = msg
        return jpeg.tobytes()

    def startTimer(self, sec):
        self.ishold = False
        while sec:
            print('timer')
            time.sleep(1)            
            sec -= 1
        print('returned')
        self.ishold = False