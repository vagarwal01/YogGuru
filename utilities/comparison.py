import cv2, base64, io
import numpy as np
from imageio import imread
import mediapipe as mp
import matplotlib.pyplot as plt

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils

class DetectionModel:
    def detectPose(image):
        # print('detect pose')
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
        output_image = image.copy()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(imageRGB)
        height, width, _ = image.shape
        landmarks = []
        if results.pose_landmarks:
            # print('detected')
            mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS)
            for landmark in results.pose_landmarks.landmark:
                landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                    (landmark.z * width)))
        # print('plotting')
        # plt.figure(figsize=[22,22])
        # plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off')
        # plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off')
        # plt.show()
        return output_image, landmarks

    def getFrame(image_string):
        # print('get frame func')
        img = imread(io.BytesIO(base64.b64decode(image_string)))
        cvImage = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cvImage = cv2.flip(cvImage, 1)
        # print('getting landmarks')
        # frame, landmarks = Detection.detectPose(cvImage)
        # print(landmarks)
        return DetectionModel.detectPose(cvImage)

class GradingModel:
    eucld_tresh = 0
    rotation_tresh = 0
    model_features = []
    input_features = []

    def __init__(self):
        self.eucld_tresh = 0.15
        self.rotation_tresh = 40

    def poseGrading(self, model, image):
        # _, self.model_features = Detection.detectPose(model)    
        _, self.model_features = DetectionModel.getFrame(model)    
        _, self.input_features = DetectionModel.getFrame(image)

        # Normalising the features
        self.model_features = self.feature_scaling(self.model_features)
        self.input_features = self.feature_scaling(self.input_features)
            
        # Splitting features in three parts
        (model_face, model_torso, model_legs) = self.split_in_face_legs_torso(self.model_features)
        (input_face, input_torso, input_legs) = self.split_in_face_legs_torso(self.input_features)

        # finding the transformation matrix and the corresponding image of input
        # (input_transformed_face,  A_face)   = self.affine_transformation(model_face,input_face)
        (input_transformed_torso, A_torso)  = self.affine_transformation(model_torso,input_torso)
        (input_transformed_legs,  A_legs)   = self.affine_transformation(model_legs,input_legs)

        # getting the parameters
        # (max_distance_face, rotation_face) = self.max_distance_and_rotation(model_face, input_transformed_face, A_face)
        (max_distance_torso, rotation_torso) = self.max_distance_and_rotation(model_torso, input_transformed_torso, A_torso)
        (max_distance_legs, rotation_legs)   = self.max_distance_and_rotation(model_legs, input_transformed_legs, A_legs)


        # Evaluating the parameters
        # result_face = self.decide_face(max_distance_face, rotation_face)
        result_torso = self.decide_torso(max_distance_torso, rotation_torso)
        result_legs  = self.decide_legs(max_distance_legs, rotation_legs)

        if(result_torso and result_legs):
            result = True
            # errorPercentage = round(((max_distance_torso + max_distance_legs)/2.0*100), 2)
            # print('error', errorPercentage)
            # accuracy_score = 100.00 - errorPercentage
        else:
            result = False
            # accuracy_score = 0
            
        errorPercentage = round(((max_distance_torso + max_distance_legs)/2.0*100), 2)
        print('error', errorPercentage)
        accuracy_score = 100.00 - errorPercentage

        # print(result, accuracy_score)
        return result, accuracy_score
        # print('% error:', round(error_score*100, 2))


    def feature_scaling(self, input):
        input = np.array(input)
        xmax = max(input[:, 0])
        ymax = max(input[:, 1])

        xmin = np.min(input[np.nonzero(input[:,0])]) #np.nanmin(input[:, 0])
        ymin = np.min(input[np.nonzero(input[:,1])]) #np.nanmin(input[:, 1])

        sec_x = (input[:, 0]-xmin)/(xmax-xmin)
        sec_y = (input[:, 1]-ymin)/(ymax-ymin)

        output = np.vstack([sec_x, sec_y]).T
        output[output<0] = 0
        return output


    def split_in_face_legs_torso(self, features):
    #     torso = features[11:23]
        torso = features[11:17]
        legs = features[23:33]
        face = np.vstack([features[0], features[1:11]])
        return (face, torso, legs)


    def affine_transformation(self, model_f, input_f):
        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
        unpad = lambda x: x[:, :-1]
        
        input_counter = 0
        nan_indices = []
        Y = pad(np.array(model_f))
        X = pad(np.array(input_f))
        A, res, rank, s = np.linalg.lstsq(X, Y, rcond=None)                         
        transform = lambda x: unpad(np.dot(pad(np.array(x)), A))
        
        input_transform = transform(input_f)
        input_transform_list  = input_transform.tolist()
        
        for index in nan_indices:
            input_transform_list.insert(index, [0,0])
        input_transform = np.array(input_transform_list)    
        A[np.abs(A) < 1e-10] = 0  # set really small values to zero
        
        return (input_transform, A)

    def max_distance_and_rotation(self, model, transformed_input, transformation_matrix):
        diff_distance = np.abs(model - transformed_input)
        euclidean_distance = ((diff_distance[:, 0]) ** 2 + diff_distance[:, 1] ** 2) ** 0.5
        max_distance = max(euclidean_distance)
    #     max_distance_landmark = np.where(euclidean_distance==max_distance)[0][0]

        rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
        rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
        max_rotation = max(rotation_2, rotation_1)

        return (max_distance, max_rotation)

    def decide_face(self, max_distance, max_rotation):
        # print(" --- Evaluate Face---")
        # print(" max eucldis:", max_distance, "thresh:", self.eucld_tresh)
        # print(" max rot:", max_rotation, "thresh:", self.rotation_tresh)

        if (max_distance <= self.eucld_tresh and max_rotation <= self.rotation_tresh):
            print("FACE MATCH\n")
            return True

        print("FACE NO-MATCH\n")
        return False

    def decide_torso(self, max_distance, max_rotation):
        # print(" --- Evaluate Torso---")
        # print(" max eucldis:", max_distance, "thresh:", self.eucld_tresh)
        # print(" max rot:", max_rotation, "thresh:", self.rotation_tresh)

        if (max_distance <= self.eucld_tresh and max_rotation <= self.rotation_tresh):
            print("TORSO MATCH\n")
            return True

        print("TORSO NO-MATCH\n")
        return False

    def decide_legs(self, max_distance, max_rotation):
        # print(" --- EvaluaEte Legs---")
        # print(" max eucldis:", max_distance, "thresh:", self.eucld_tresh)
        # print(" max rot:", max_rotation, "thresh:", self.rotation_tresh)

        if (max_distance <= self.eucld_tresh and max_rotation <= self.rotation_tresh):
            print("LEGS MATCH\n")
            return True

        print("LEGS NO-MATCH\n")
        return False





# image = cv2.imread('imgs/tree/tree-11.jpeg')
# _, model_features = detectPose(image, pose, display=True)