import time
import sys
import cv2
import psutil
from ml import Movenet
from data import BodyPart
import utils
import moter
import shoot

def is_person_detected(person, detection_threshold=0.5):
    return person.score > detection_threshold

def check_arm_positions(pose):
    head = pose.keypoints[BodyPart.NOSE.value].coordinate
    rw = pose.keypoints[BodyPart.RIGHT_WRIST.value].coordinate
    lw = pose.keypoints[BodyPart.LEFT_WRIST.value].coordinate
    
    global degree 
    degree = head.x

    if not is_person_detected(pose):
        return "No Person"
    
    elif lw.y > head.y and rw.y > head.y:
        return "No Hand (wait)"
    
    elif lw.y > head.y or rw.y > head.y:
        return "One Hand (Move)"
    else:
        return "Both Hand (Shoot)"

def print_system_info():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_percent}%")
    
def print_reaction_time(start_time, end_time):
    reaction_time = (end_time - start_time) * 1000
    print("%.2fms\n" %reaction_time)

def main():
    estimation_model = 'movenet_lightning'
    camera_id = 0
    width = 640
    height = 480

    pose_detector = Movenet(estimation_model)

    try:
        while True:
            start_time = time.time()
            
            # 카메라 동작 시작
            cap = cv2.VideoCapture(camera_id)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            success, image = cap.read()
            if not success:
                sys.exit(
                    'ERROR: Unable to read from camera.'
                )

             
            # 포즈 추정 수행
            list_persons = [pose_detector.detect(image)]

            if list_persons:
                for i, person in enumerate(list_persons):
                    arm_position = check_arm_positions(person)
                    print(arm_position)

                    # 영상 띄우기 비활성화
                    # image = utils.visualize(image, [person])

                # cv2.imshow('Pose Estimation', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            end_time = time.time()
            
            print_system_info()
            print_reaction_time(start_time, end_time)
            
            cap.release()

            if arm_position == "No Person":
                continue

            elif arm_position == "One Hand (Move)" and (degree < 280 or degree > 360):
                if degree < 280: 
                    print(degree)
                    moter.rotateAntiClockwise()

                elif degree > 360:
                    print(degree)
                    moter.rotateClockwise()

            elif arm_position == "Both Hand (Shoot)":
                shoot.take_photo()
            

    except KeyboardInterrupt:
        # ctrl + c 로 중단
        pass

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()