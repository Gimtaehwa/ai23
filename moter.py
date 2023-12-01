import RPi.GPIO as GPIO 
from time import sleep  

# GPIO 핀 설정
servoPin = 12  
GPIO.setmode(GPIO.BOARD)        
GPIO.setup(servoPin, GPIO.OUT)  

servo = GPIO.PWM(servoPin, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo.start(0) 


def setServoPos(dutyCycle):

      GPIO.setup(servoPin, GPIO.OUT)

      servo.ChangeDutyCycle(dutyCycle)

      sleep(0.1)

      GPIO.setup(servoPin, GPIO.IN)
      
  
def rotateClockwise():
      setServoPos(6.5)
      # 시계방향 약 5도 회전
      
def rotateAntiClockwise():
      setServoPos(7.5)
      # 반시계방향 약 5도 회전
      
if __name__ == "__main__":
      rotateClockwise()
      GPIO.cleanup()