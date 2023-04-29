# Smart Surveillance Parking Camera
# Supervisor: Dr. Raghavendra Bhalerao
# Jeet Pranav      Satyajeet K Verma   (2022)
from calendar import c
from cv2 import FONT_HERSHEY_SCRIPT_SIMPLEX
import numpy                                                                                                
import cv2 
from cv2 import FONT_HERSHEY_TRIPLEX
import Utils as ut
import screen_brightness_control as sbc
from datetime import datetime as DTX
from pyfirmata import Arduino
import matplotlib.pyplot as plt
import matplotlib.path as MPL
board = Arduino('COM8')

lstcx = []
lstcy = []                        
     
#Toggle Function
def toggle(x):
 RELAY=[2,3,4,5,6,7,8,9,10]
 board.digital[x].write(1)
 RELAY.remove(x)
 for i in RELAY:
   board.digital[i].write(0)
def row(a,b,c,d,e,f,g,h,i):

  #ON
  board.digital[a].write(1)
  board.digital[b].write(1)
  board.digital[c].write(1)
  #OFF
  board.digital[d].write(0)
  board.digital[e].write(0)
  board.digital[f].write(0)
  board.digital[g].write(0)
  board.digital[h].write(0)
  board.digital[i].write(0)
                                                                                                               
cap = cv2.VideoCapture("J:\BTP\Sem 8\Footage and Raw\inight6.mp4")                                                   #loading the video
ret,frame1 = cap.read()                                                                                               # fetching 2 frames from the loaded video
ret,frame2 = cap.read()
Height=frame1.shape[0]
Width=frame1.shape[1]
res = str("Video Resolution: ") + str(Height) + str(" x ")+ str(Width)

# TRACKBARS
cv2.namedWindow('controls')
val = sbc.get_brightness()
def Track(x):
	sbc.set_brightness(x)    
def Track2(y):
    toggle(y)
    pass
cv2.createTrackbar('Brightness','controls', 0 , 255, Track)
cv2.createTrackbar('M Relay','controls', 1 , 9, Track2)


while cap.isOpened():   
    #Pre-Processing  
    diff = cv2.absdiff(frame1,frame2)                                                                              
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)                                                    
    blur = cv2.GaussianBlur(gray,(5,5), 1)
    _,thresh= cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)
    dilate = cv2.dilate(thresh, None, iterations=22)   
    #Trackbars
    xbgt = cv2.getTrackbarPos('Brightness','controls')
    xrelay = cv2.getTrackbarPos('M Relay','controls')
    #Warp Perspective
    pts1=numpy.float32([[145,830],[455,821],[1,1513],[862,1441]])
    pts2=numpy.float32([[0,0],[400,0],[0,400],[400,400]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)  
    output=cv2.warpPerspective(frame1,matrix,(400,400)) 
    #Text on Screens
    cv2.putText(output,'Object In Perspective', (60, 380), FONT_HERSHEY_TRIPLEX, 0.8, (0, 255, 0), 2,cv2.LINE_4)
    now = DTX.now().time()
    now = str(now)
    cv2.putText(output,now, (285, 30), FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0), 1,cv2.LINE_4)
    cv2.putText(frame1,res, (35, 1700), FONT_HERSHEY_TRIPLEX, 1.2, (0, 255, 0), 2,cv2.LINE_4)
    cv2.imshow("Warp Perspective : Flat Output", output)
    #Boundary Lines
    cv2.line(frame1, (145,830), (455,821), (0, 0, 255), 4)
    cv2.line(frame1, (455,821), (862,1441), (0, 0, 255), 4)
    cv2.line(frame1, (862,1441), (1,1513), (0, 0, 255), 4)
    cv2.line(frame1, (1,1513), (145,830), (0, 0, 255), 4)
    #Divider Lines
    cv2.line(frame1, (104,1009), (566,990), (0, 0, 255), 4)
    cv2.line(frame1, (62,1200), (680,1160), (0, 0, 255), 4)

    #For demonstration purpose, we have manually defined the fences
    #Ranges
    h1= numpy.arange(832,1000)
    h2= numpy.arange(1000,1150)
    h3= numpy.arange(1150,1515) 
    fault = numpy.arange(2,832)
    
    #Contour Detection
    contours,_ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                    
    for contour in contours:      
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"]) 
        lstcx.append(cX)
        lstcy.append(cY)   
        #Conditions                                                                                # only allowing contours bigger than 5000 units of area
        if cv2.contourArea(contour)<11500 :
            continue
        if cY not in fault:
            (x, y, w, h) = cv2.boundingRect(contour)                                                                      #to draw a rectangle frame around the allowed(>5000) contour
            cv2.rectangle(frame1, (x,y), (x+w,y+h), (0, 255, 100), 5)
            cv2.circle(frame1, (cX, cY), 13, (0, 0, 255), -1) 
            print(cv2.contourArea(contour))
        #Main Decision Making Ladder
        if cY in h1:
            row(2,3,4,5,6,7,8,9,10)
            print("1")
            cv2.putText(frame1,'REGION 1/3 ', (50, 70), FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 3,cv2.LINE_4)
        elif cY in h2:
            row(5,6,7,2,3,4,8,9,10)
            print("2")
            cv2.putText(frame1,'REGIONw 2/3 ', (50, 70), FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 3,cv2.LINE_4)
        elif cY in h3:
            row(8,9,10,2,3,4,5,6,7)
            print("3")
            cv2.putText(frame1,'REGION 3/3 ', (50, 70), FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 3,cv2.LINE_4)
        elif cY in fault:
            pass   
        elif cv2.contourArea(contour) > 1042344:
            row(8,9,10,2,3,4,5,6,7)
            
        else:
            pass 
        
    #Display                                                                                                                       # draw the center of the shape on the image
    resize = cv2.resize(frame1, (500,700))                                                                           #because the video wasnt fitting the screen
    cv2.imshow("Smart Surveillance Parking Camera", resize)                                                                               
    frame1 = frame2                                                   
    ret, frame2 = cap.read()                                                                                          # to fetch and display the final frame, not the processed, the processed one has all sorts of filters applied to it which the user doesnt need to see.the user wants the processed output in the ORIGINAL frame which is nothing but frame1 and frame2
    if cv2.waitKey(1) & 0xFF == 27:                                                                             # sets the FPS, and the exit key
        break
cap.release()                                                                                                         #to stop loading
cv2.destroyAllWindows()                                                                                               #to destroy all the imshow windows (here, only one window as only   one imshow has been called)
print(lstcx)        
plt.scatter(lstcx,lstcy) 
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("CENTROID OF THE DETECTED CONTOURS IN SPATIAL DOMAIN (AUTO_SCALED)")                                        #plt.autoscale(False) plt.xlim(0,100000) plt.ylim(0,800)
plt.show()

