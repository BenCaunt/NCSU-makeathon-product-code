import detector
import arduino_coms
import cv2
cap = cv2.VideoCapture(0)
arduino = arduino_coms.ArduinoCommunicator(port='/dev/tty.usbmodem1101',baudrate=9600)

print("starting loop")
while True:
    if arduino.listen_for_pedal_press():
        bin = detector.capture_frame_and_assess(cap)
        arduino.send_message(bin)

cap.release()
cv2.destroyAllWindows()
