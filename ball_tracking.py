# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages

from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import pipes
import sys

toggle = True

maxPos = 1000
minPos = 0

new_user = "hello"
#result = firebase.post('/positions', maxPos, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})

# Firebase authenticate


# Set current time
now = time.time()


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=6,
    help="max buffer size")
ap.add_argument("-g", "--green", help="color", default="g")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0,0,0)
greenUpper = (0,0,0)

if args["green"] == "g":
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
else:
    #greenLower = (168,1,84)
    #greenUpper = (255, 186, 220)
    greenLower = (132,35,75)
    greenUpper = (255, 160, 182)
    #greenLower = (95,73,147)
    #greenUpper = (188, 107, 191)
    
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    #time.sleep(0.01)
    currentTime = time.time()
    timeDiff = round(currentTime - now,3)
    
    
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        # Callibration
        
        
        if timeDiff < 12:

            if y < maxPos:
                maxPos = y
                print "Set max Position to {}".format(maxPos)
                
            if y > minPos:
                minPos = y
                print "Set min Position to {}".format(minPos)
        else:
            if toggle:
                print "Go."
                toggle = False
                
            numberOfPos = minPos - maxPos + 1
            percentage = (y - maxPos) / numberOfPos
            
            if percentage < 0:
                percentage = 0
            if percentage > 1:
                percentage = 1

            if args["green"] == "g":
                f = pipes.Template().open('percent1.txt', 'w')
                f.write("{}".format(percentage))
            else:     
                f = pipes.Template().open('percent2.txt', 'w')
                f.write("{}".format(percentage))

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
f.close()
camera.release()
cv2.destroyAllWindows()