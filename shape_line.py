import cv2 as cv
import numpy as np

url1 = 'http://192.168.91.194:8080/video'
url2 = 'http://192.168.1.105:8080/video'


cap1 = cv.VideoCapture(url1)
# cap2 = cv.VideoCapture(url2)
cap1.set(cv.CAP_PROP_FPS, 30)
# cap2.set(cv.CAP_PROP_FPS, 30)

def empty(img):
    pass

cv.namedWindow("TrackBar")
cv.resizeWindow("TrackBar", 600, 300)
# cv.createTrackbar("hue_min", "TrackBar", 0, 179, empty)
# cv.createTrackbar("hue_max", "TrackBar", 179, 179, empty)
# cv.createTrackbar("sat_min", "TrackBar", 0, 255, empty)
# cv.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
# cv.createTrackbar("val_min", "TrackBar", 0, 255, empty)
# cv.createTrackbar("val_max", "TrackBar", 255, 255, empty)
cv.createTrackbar("thresh1", "TrackBar", 0, 255, empty)
cv.createTrackbar("thresh2", "TrackBar", 255, 255, empty)
cv.createTrackbar("Area", "TrackBar", 200, 10000, empty)

### create the ranges of the colors
# lower_red = np.array([160, 149, 180])
# upper_red = np.array([180, 255, 255])
# lower_blue = np.array([110, 50, 50])
# upper_blue = np.array([130, 255, 255])
# lower_green = np.array([0, 149, 180])
# upper_green = np.array([180, 255, 255])
lower_black = np.array([0, 0, 0])
upper_black = np.array([50, 50, 50])

# Create an empty dictionary to store object IDs and their contours
object_dict = {}
circles, squares, triangles, rectangles = 0, 0, 0, 0
def check_id(contour, object_id_counter):
        """this is a function that check if the id of the seen shape is calculated or not"""
        # Calculate the center of the contour
        M = cv.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Check if an object with similar centroid already exists
            existing_object_id = None
            for obj_id, (prev_cX, prev_cY) in object_dict.items():
                distance = ((cX - prev_cX) ** 2 + (cY - prev_cY) ** 2) ** 0.5
                if distance < 20:  # Adjust this threshold as needed
                    existing_object_id = obj_id
                    break

            # Assign a new object ID or update the existing one
            if existing_object_id is None:
                object_id_counter += 1
                object_dict[object_id_counter] = (cX, cY)


def get_contours(img, imgContour):
    """ this is a function that takes the mask and the frame and it extracts the contours from the mask and draw it in the frame"""
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Loop through detected contours
    for cnt in contours:
        area = cv.contourArea(cnt)
        minArea = cv.getTrackbarPos("Area", "TrackBar")
        if area > minArea:
            cv.drawContours(imgContour, cnt, -1, (0,255,0), 1)
            # Approximate the contour to a polygon
            epsilon = 0.04 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)
            print(len(approx))
            x, y, w, h = cv.boundingRect(cnt)


            if len(approx) == 4: 
                aspect_ratio = float(w) / h
                cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                cv.putText(imgContour, f"points: {approx}" ,(x+w+20, y+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                cv.putText(imgContour, f"area: {cv.contourArea(cnt)}" ,(x+w+20, y+40), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                if aspect_ratio >= 0.9 and aspect_ratio <= 1.1:
                    cv.putText(imgContour, f"Shape: Square" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)
                    check_id(cnt, squares)
                else:
                    cv.putText(imgContour, f"Shape: Rectangle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)
                    check_id(cnt, rectangles)

            if len(approx) == 3:
                cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                cv.putText(imgContour, f"points: {approx}" ,(x+w+20, y+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                cv.putText(imgContour, f"Shape: Triangle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)
                check_id(cnt, triangles)

            if len(approx) > 7 and len(approx) < 16:
                cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                cv.putText(imgContour, f"Shape: Circle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)
                check_id(cnt, circles)



while True:
    #-------------shape detection------------------
    ret1, frame1 = cap1.read()
    # ret2, frame2 = cap2.read()

    # if (not ret1) or (not ret2):
    #     break

    frame1 = cv.resize(frame1, (540, 960))
    # frame2 = cv.resize(frame2, (540, 960))
    
    blur_img = cv.GaussianBlur(frame1, (7,7), 2)
    gray_img = cv.cvtColor(blur_img, cv.COLOR_BGR2GRAY)

    threshold1 = cv.getTrackbarPos("thresh1", "TrackBar")
    thershold2 = cv.getTrackbarPos("thresh2", "TrackBar")
    ret, thresh = cv.threshold(gray_img, threshold1, thershold2, cv.THRESH_BINARY_INV)

    canny_img = cv.Canny(thresh, threshold1, thershold2)

    kernal = np.ones((5,5), np.uint8)
    dilate = cv.dilate(canny_img, kernal, iterations=1)

    get_contours(dilate, frame1)

    cv.imshow("dilate", dilate)
    cv.imshow("canny", canny_img)
    cv.imshow("frame1_copy", frame1)

    #--------------line follower--------------------
    # if button_clicked:

    # BlackLine = cv.inRange(frame2, lower_black, upper_black) # create the mask
    # kernel = np.ones((5,5), np.uint8)
    # BlackLine = cv.erode(BlackLine, kernel, iterations=1) # apply some morophological operational
    # BlackLine = cv.dilate(BlackLine, kernel, iterations=2)

    # contoursBlk, hierarchyBlk = cv.findContours(BlackLine, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # if len(contoursBlk) > 0:
    #     biggest_contour = max(contoursBlk, key = cv.contourArea)
    #     blackbox = cv.minAreaRect(biggest_contour) 
    #     (x_min, y_min), (w_min, h_min), ang = blackbox
    #     setPoint = 480 # the set point is the half of the camera's resolution = 960/2
    #     error = int(x_min) - setPoint # center line of the black line -  set Point
    #     ang = int(ang)                
    #     # send the values of error and angles here

    #     box = cv.boxPoints(blackbox)
    #     box = np.int0(box)
    #     cv.drawContours(frame2, [box], 0, (0,255,0), 2)
    #     cv.putText(frame2, str(ang), (10, 40), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #     cv.putText(frame2, str(error), (10, 500), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    #     cv.line(frame2, (int(x_min), 200), (int(x_min), 250 ), (255,0,0), 3)
    #     cv.line(frame2, (int(x_min) , 200), (setPoint, 200), (0,255,0), 3)
                
    #     cv.imshow("mask", BlackLine)
    #     cv.imshow("result", frame2)
    #-----------------------------------------------------------------------------------------------------



    # Press Esc key to exit
    if cv.waitKey(1) == 27:
        break

print(f"circles {circles}\nsquares {squares}\nrectangles {rectangles}\ntriangles {triangles}\n")
cap1.release()
# cap2.release()
cv.destroyAllWindows()
