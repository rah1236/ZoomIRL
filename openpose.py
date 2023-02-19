# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np
import argparse
import math
import serial
import struct
import time

ser = serial.Serial('/dev/cu.usbmodem101', 9600, write_timeout = 1) # Change 'COM3' to the appropriate port name for your system

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')

args = parser.parse_args()



font                   = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2


def getAngle(partA, partB):

    if partA is not None and partB is not None:
        if points[partA] is not None and points[partB] is not None:
            return math.atan2(points[partA][1] - points[partB][1],points[partA][0] - points[partB][0])*180/math.pi

neckAngle = 0
LshoulderAngle = 0
RshoulderAngle = 0
headAngle = 0

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width
inHeight = args.height

net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

cap = cv.VideoCapture(args.input if args.input else 0)
dataSendCount = 0

while cv.waitKey(1) < 0:
    dataSendCount += 1


    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])
    points = []

    #if dataSendCount == 10:
       # if not ser.isOpen():
           # ser.open()
        #for i in range(4):
    
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > args.thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.putText(frame,str(idTo), 
    points[idTo], 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

            if getAngle(BODY_PARTS["Neck"],BODY_PARTS["Nose"]) is not None: neckAngle = int(getAngle(BODY_PARTS["Neck"],BODY_PARTS["Nose"])) 
            if getAngle(BODY_PARTS["LShoulder"],BODY_PARTS["Neck"]) is not None: LshoulderAngle = int(getAngle(BODY_PARTS["LShoulder"],BODY_PARTS["Neck"]))+90
            if getAngle(BODY_PARTS["RShoulder"],BODY_PARTS["Neck"]) is not None: RshoulderAngle = int(getAngle(BODY_PARTS["Neck"],BODY_PARTS["RShoulder"])) +90
            if getAngle(BODY_PARTS["LEye"],BODY_PARTS["REye"]) is not None: headAngle = int(getAngle(BODY_PARTS["LEye"],BODY_PARTS["REye"]))+90



            print("Neck angle ",neckAngle)
            print("Neck Right Shoulder Angle: ", RshoulderAngle)
            print("Neck Left Shoulder Angle: ", LshoulderAngle)
            print("Head Angle: ", headAngle)
            values = [neckAngle,LshoulderAngle,RshoulderAngle,headAngle]
            #scaled_values = [int(value * 2**7) for value in values]
            #ser.open()
    thingOut = struct.pack('>q',  neckAngle + (LshoulderAngle<<16) + (RshoulderAngle << 32) + (headAngle<<48))
    print("should>neck    BYTE OUT: ", thingOut)
   # ser.write(struct.pack('>l',  neckAngle + (LshoulderAngle<<16))) # Shift the data left by 1 bit and pack it into 2 bytes
    #ser.flush() # Wait for all data to be sent
    ser.write(thingOut) #+ (RshoulderAngle<<) + (headAngle<<32))) # Shift the data left by 1 bit and pack it into 2 bytes

    time.sleep(0.0005)
    # ser.write(struct.pack('>h', LshoulderAngle))
    # ser.flush() # Wait for all data to be sent
    # time.sleep(0.000125)
        

            









    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv.imshow('OpenPose using OpenCV', frame)