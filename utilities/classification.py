import mediapipe as mp
import matplotlib.pyplot as plt


mp_pose = mp.solutions.pose # Initializing mediapipe pose class.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils # Initializing mediapipe drawing class, useful for annotation.



class Classification1:
    def classifyTreePose(angles, landmarks):
        msg = 'stand straight'
        # Check if one leg is straight
        if angles['left_knee_angle'] > 150 and angles['left_knee_angle'] < 200 or angles['right_knee_angle'] > 150 and angles['right_knee_angle'] < 200:
            # Check if the other leg is bended at the required angle.
            if angles['left_knee_angle'] > 260 or angles['right_knee_angle'] < 100:
                # Check if arms are upward
                if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                    # Check if hands are joined
                    x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                    x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                    if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                        # Check if arms are straight
                        if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                            msg = 'success'

                        else:
                            msg = 'arms must be straight'         
                    else:
                        msg = 'join your hands together'
                else:
                    msg = 'move your arms upward'
            else:
                msg = 'put your one foot on another knee'
        else:
            msg = 'stand straight'

        return msg


    def classifyBridgePose(angles, landmarks):
        text = 'Lie down on the floor'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value][1]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value][1]

        # Check if person is lie down
        if (abs(ls-lh)>0 and abs(ls-lh)<60) or (abs(rs-rh)>0 and abs(rs-rh)<60):
            # Check if knees are bend
            if (angles['left_knee_angle'] > 45 and angles['left_knee_angle'] < 90 and angles['right_knee_angle'] > 45 and angles['right_knee_angle'] < 90) or (angles['left_knee_angle'] > 270 and angles['left_knee_angle'] < 315 and angles['right_knee_angle'] > 270 and angles['right_knee_angle'] < 315):
                # Check if hips are up
                if angles['left_hip_angle'] > 145 or angles['right_hip_angle'] > 145:
                    # Check if hands are inside
                    if (angles['left_shoulder_angle'] < 60 and angles['right_shoulder_angle'] < 330) or (angles['left_shoulder_angle'] < 330 and angles['right_shoulder_angle'] < 60):
                        # Check if hands are straight
                        if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                            text = "success"
                        else:
                            text = "Keep your hands straight"
                    else:
                        text = "Keep your hands inside"
                else:
                    text = "Move your hips upward"
            else:
                text = "Bend your knees"
        else:
            text = "Lie down on the floor"

        return text


    def classifyWarrior1Pose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyWarrior1PoseRight(angles, landmarks)
        else:
            return Classification1.classifyWarrior1PoseLeft(angles, landmarks)
    def classifyWarrior1PoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['right_knee_angle'] > 100 and angles['right_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the other leg is bended at the required angle.
                if angles['left_knee_angle'] > 230 and angles['left_knee_angle'] < 290:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are upwards
                        if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                            # Check if hands are joined
                            x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                            x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                            if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                                # Check if arms are straight
                                if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                                    msg = 'success'

                                else:
                                    msg = 'arms must be straight'         
                            else:
                                msg = 'join your hands together'
                        else:
                            msg = 'move your arms upwards'
                    else:
                        msg = 'slightly move your right ankle more foward'
                else:
                    msg = 'slightly bend your right leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg
    def classifyWarrior1PoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['left_knee_angle'] > 100 and angles['left_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the other leg is bended at the required angle.
                if angles['right_knee_angle'] > 70 and angles['right_knee_angle'] < 130:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are upwards
                        if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                            # Check if hands are joined
                            x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                            x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                            if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                                # Check if arms are straight
                                if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                                    msg = 'success'

                                else:
                                    msg = 'arms must be straight'         
                            else:
                                msg = 'join your hands together'
                        else:
                            msg = 'move your arms upwards'
                    else:
                        msg = 'slightly move your left ankle more foward'
                else:
                    msg = 'slightly bend your left leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg


    def classifyWarrior2Pose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyWarrior2PoseRight(angles, landmarks)
        else:
            return Classification1.classifyWarrior2PoseLeft(angles, landmarks)
    def classifyWarrior2PoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['right_knee_angle'] > 100 and angles['right_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the right leg is bended at the required angle.
                if angles['left_knee_angle'] > 230 and angles['left_knee_angle'] < 290:
                    # Check if bended leg position is accurate
                    ra = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
                    rk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0]
                    if abs(ra-rk) < 20:
                        # Check if arms are sidewards
                        if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120 and angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                            # Check if arms are straight
                            if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                                msg = 'success'
                            else:
                                msg = 'arms must be straight'         
                        else:
                            msg = 'move your arms sidewards'
                    else:
                        msg = 'slightly move your right ankle more foward'
                else:
                    msg = 'slightly bend your right leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg
    def classifyWarrior2PoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['left_knee_angle'] > 100 and angles['left_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the left leg is bended at the required angle.
                if angles['right_knee_angle'] > 70 and angles['right_knee_angle'] < 130:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are sidewards
                        if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120 and angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                            # Check if arms are straight
                            if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                                msg = 'success'
                            else:
                                msg = 'arms must be straight'         
                        else:
                            msg = 'move your arms sidewards'
                    else:
                        msg = 'slightly move your left ankle more foward'
                else:
                    msg = 'slightly bend your left leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg


    def classifyTrianglePose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyTrianglePoseRight(angles, landmarks)
        else:
            return Classification1.classifyTrianglePoseLeft(angles, landmarks)
    def classifyTrianglePoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if both legs are straight
        if angles['right_knee_angle'] > 150 and angles['right_knee_angle'] < 210 and angles['left_knee_angle'] > 150 and angles['left_knee_angle'] < 210:
            # Check if there is sufficient distance between legs
            if abs(la-ra) >= abs(ls-rs)*2:
                # Check if arms are sidewards
                if angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                    # Check if arms are straight
                    if angles['left_elbow_angle'] > 150 and angles['left_elbow_angle'] < 210 and angles['right_elbow_angle'] > 150 and angles['right_elbow_angle'] < 210:
                        # Check if right arm is downward
                        ra = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][1]
                        rw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][1]
                        rk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][1]
                        if rw > rk or abs(rw-rk) <= 50:
                            msg = 'success'
                        else:
                            msg = 'move your right arm downwards'
                    else:
                        msg = 'arms must be straight'         
                else:
                    msg = 'stretch your arms sidewards'
            else:
                msg = 'widen the gap between the legs'
        else:
            msg = 'keep your legs straight'

        return msg
    def classifyTrianglePoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if both legs are straight
        if angles['right_knee_angle'] > 150 and angles['right_knee_angle'] < 210 and angles['left_knee_angle'] > 150 and angles['left_knee_angle'] < 210:
            # Check if there is sufficient distance between legs
            if abs(la-ra) >= abs(ls-rs)*2:
                # Check if arms are sidewards
                if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120:
                    # Check if arms are straight
                    if angles['left_elbow_angle'] > 150 and angles['left_elbow_angle'] < 210 and angles['right_elbow_angle'] > 150 and angles['right_elbow_angle'] < 210:
                        # Check if left arm is downward
                        la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][1]
                        lw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][1]
                        lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][1]
                        if lw > lk or abs(lw-lk) <= 50:
                            msg = 'success'
                        else:
                            msg = 'move your left arm downwards'
                    else:
                        msg = 'arms must be straight'         
                else:
                    msg = 'stretch your arms sidewards'
            else:
                msg = 'widen the gap between the legs'
        else:
            msg = 'keep your legs straight'

        return msg


class Classification2:
    def classifyTreePose(angles, landmarks):
        msg = 'stand straight'
        # Check if one leg is straight
        if angles['left_knee_angle'] > 165 and angles['left_knee_angle'] < 195 or angles['right_knee_angle'] > 165 and angles['right_knee_angle'] < 195:
            # Check if the other leg is bended at the required angle.
            if angles['left_knee_angle'] > 315 and angles['left_knee_angle'] < 350 or angles['right_knee_angle'] > 25 and angles['right_knee_angle'] < 75:
                # Check if arms are upward
                if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                    # Check if hands are joined
                    x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                    x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                    if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                        # Check if arms are straight
                        if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                            msg = 'success'

                        else:
                            msg = 'arms must be straight'         
                    else:
                        msg = 'join your hands together'
                else:
                    msg = 'move your arms upward'
            else:
                msg = 'put your one foot on another knee'
        else:
            msg = 'stand straight'

        return msg


    def classifyBridgePose(angles, landmarks):
        text = 'Lie down on the floor'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value][1]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value][1]

        # Check if person is lie down
        if (abs(ls-lh)>0 and abs(ls-lh)<60) or (abs(rs-rh)>0 and abs(rs-rh)<60):
            # Check if knees are bend
            if (angles['left_knee_angle'] > 45 and angles['left_knee_angle'] < 90 and angles['right_knee_angle'] > 45 and angles['right_knee_angle'] < 90) or (angles['left_knee_angle'] > 270 and angles['left_knee_angle'] < 315 and angles['right_knee_angle'] > 270 and angles['right_knee_angle'] < 315):
                # Check if hips are up
                if angles['left_hip_angle'] > 145 or angles['right_hip_angle'] > 145:
                    # Check if hands are inside
                    if (angles['left_shoulder_angle'] < 60 and angles['right_shoulder_angle'] < 330) or (angles['left_shoulder_angle'] < 330 and angles['right_shoulder_angle'] < 60):
                        # Check if hands are straight
                        if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                            text = "success"
                        else:
                            text = "Keep your hands straight"
                    else:
                        text = "Keep your hands inside"
                else:
                    text = "Move your hips upward"
            else:
                text = "Bend your knees"
        else:
            text = "Lie down on the floor"

        return text


    def classifyWarrior1Pose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyWarrior1PoseRight(angles, landmarks)
        else:
            return Classification1.classifyWarrior1PoseLeft(angles, landmarks)
    def classifyWarrior1PoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['right_knee_angle'] > 100 and angles['right_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the other leg is bended at the required angle.
                if angles['left_knee_angle'] > 230 and angles['left_knee_angle'] < 290:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are upwards
                        if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                            # Check if hands are joined
                            x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                            x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                            if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                                # Check if arms are straight
                                if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                                    msg = 'success'

                                else:
                                    msg = 'arms must be straight'         
                            else:
                                msg = 'join your hands together'
                        else:
                            msg = 'move your arms upwards'
                    else:
                        msg = 'slightly move your right ankle more foward'
                else:
                    msg = 'slightly bend your right leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg
    def classifyWarrior1PoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['left_knee_angle'] > 100 and angles['left_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the other leg is bended at the required angle.
                if angles['right_knee_angle'] > 70 and angles['right_knee_angle'] < 130:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are upwards
                        if angles['left_shoulder_angle'] > 145 and angles['right_shoulder_angle'] > 145:
                            # Check if hands are joined
                            x1, y1, _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                            x2, y2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                            if(abs(x1 - x2) > 0 and abs(x1 - x2) < 30 and abs(y1 - y2) > 0 and abs(y1 - y2) < 30):
                                # Check if arms are straight
                                if angles['left_elbow_angle'] > 100 and angles['right_elbow_angle'] > 100:
                                    msg = 'success'

                                else:
                                    msg = 'arms must be straight'         
                            else:
                                msg = 'join your hands together'
                        else:
                            msg = 'move your arms upwards'
                    else:
                        msg = 'slightly move your left ankle more foward'
                else:
                    msg = 'slightly bend your left leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg


    def classifyWarrior2Pose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyWarrior2PoseRight(angles, landmarks)
        else:
            return Classification1.classifyWarrior2PoseLeft(angles, landmarks)
    def classifyWarrior2PoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['right_knee_angle'] > 100 and angles['right_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the right leg is bended at the required angle.
                if angles['left_knee_angle'] > 230 and angles['left_knee_angle'] < 290:
                    # Check if bended leg position is accurate
                    ra = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
                    rk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0]
                    if abs(ra-rk) < 20:
                        # Check if arms are sidewards
                        if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120 and angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                            # Check if arms are straight
                            if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                                msg = 'success'
                            else:
                                msg = 'arms must be straight'         
                        else:
                            msg = 'move your arms sidewards'
                    else:
                        msg = 'slightly move your right ankle more foward'
                else:
                    msg = 'slightly bend your right leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg
    def classifyWarrior2PoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if one leg is straight
        if angles['left_knee_angle'] > 100 and angles['left_knee_angle'] < 220:
            # Check if there is sufficient distance between legs
            if abs(la-ra) > abs(ls-rs):
                # Check if the left leg is bended at the required angle.
                if angles['right_knee_angle'] > 70 and angles['right_knee_angle'] < 130:
                    # Check if bended leg position is accurate
                    la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]
                    lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0]
                    if abs(la-lk) < 20:
                        # Check if arms are sidewards
                        if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120 and angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                            # Check if arms are straight
                            if angles['left_elbow_angle'] > 165 and angles['left_elbow_angle'] < 195 and angles['right_elbow_angle'] > 165 and angles['right_elbow_angle'] < 195:
                                msg = 'success'
                            else:
                                msg = 'arms must be straight'         
                        else:
                            msg = 'move your arms sidewards'
                    else:
                        msg = 'slightly move your left ankle more foward'
                else:
                    msg = 'slightly bend your left leg sidewards'
            else:
                msg = 'open your legs'
        else:
            msg = 'stand straight'

        return msg


    def classifyTrianglePose(side, angles, landmarks):
        if side == 'R':
            return Classification1.classifyTrianglePoseRight(angles, landmarks)
        else:
            return Classification1.classifyTrianglePoseLeft(angles, landmarks)
    def classifyTrianglePoseRight(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if both legs are straight
        if angles['right_knee_angle'] > 150 and angles['right_knee_angle'] < 210 and angles['left_knee_angle'] > 150 and angles['left_knee_angle'] < 210:
            # Check if there is sufficient distance between legs
            if abs(la-ra) >= abs(ls-rs)*2:
                # Check if arms are sidewards
                if angles['right_shoulder_angle'] > 70 and angles['right_shoulder_angle'] < 120:
                    # Check if arms are straight
                    if angles['left_elbow_angle'] > 150 and angles['left_elbow_angle'] < 210 and angles['right_elbow_angle'] > 150 and angles['right_elbow_angle'] < 210:
                        # Check if right arm is downward
                        ra = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][1]
                        rw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][1]
                        rk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][1]
                        if rw > rk or abs(rw-rk) <= 50:
                            msg = 'success'
                        else:
                            msg = 'move your right arm downwards'
                    else:
                        msg = 'arms must be straight'         
                else:
                    msg = 'stretch your arms sidewards'
            else:
                msg = 'widen the gap between the legs'
        else:
            msg = 'keep your legs straight'

        return msg
    def classifyTrianglePoseLeft(angles, landmarks):
        msg = 'stand straight'

        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0]
        la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0]
        ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0]

        # Check if both legs are straight
        if angles['right_knee_angle'] > 150 and angles['right_knee_angle'] < 210 and angles['left_knee_angle'] > 150 and angles['left_knee_angle'] < 210:
            # Check if there is sufficient distance between legs
            if abs(la-ra) >= abs(ls-rs)*2:
                # Check if arms are sidewards
                if angles['left_shoulder_angle'] > 70 and angles['left_shoulder_angle'] < 120:
                    # Check if arms are straight
                    if angles['left_elbow_angle'] > 150 and angles['left_elbow_angle'] < 210 and angles['right_elbow_angle'] > 150 and angles['right_elbow_angle'] < 210:
                        # Check if left arm is downward
                        la = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][1]
                        lw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][1]
                        lk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][1]
                        if lw > lk or abs(lw-lk) <= 50:
                            msg = 'success'
                        else:
                            msg = 'move your left arm downwards'
                    else:
                        msg = 'arms must be straight'         
                else:
                    msg = 'stretch your arms sidewards'
            else:
                msg = 'widen the gap between the legs'
        else:
            msg = 'keep your legs straight'

        return msg

