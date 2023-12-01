import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from datetime import datetime

# GPIO 핀 번호 설정
led_pin = 40

def led_count():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led_pin, GPIO.OUT)
    
    # 1초씩 sleep
    for i in range(3):
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(0.5)

def take_photo():
    # 현재 시각을 이용하여 파일 경로 생성
    current_time = datetime.now()
    file_name = current_time.strftime("%Y%m%d_%H%M%S") + ".jpg"
    file_path = "/home/pi/server/static/images/" + file_name
    
    camera = PiCamera()

    try:
        # 사진 찍기 전에 LED 카운트
        led_count()

        # 사진 찍기
        camera.start_preview()
        camera.capture(file_path)
        print(f"사진이 {file_path}에 저장되었습니다.")
    finally:
        # 리소스 해제
        camera.stop_preview()
        camera.close()
        GPIO.cleanup()

if __name__ == "__main__":
    take_photo()