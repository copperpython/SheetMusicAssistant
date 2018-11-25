# test on how to read, display, and write images
import cv2
import numpy as np
import Notes
from Sounds import sounds
import time
import threading
from threading import Thread

def deduplicate(allPoints, bounds=10):
    # takes in allPoints list of tuples from locations(),
    # and returns a list of tuples that is deduplicated

    # sort the tuples based on x and y coordinates in ascending order
    sortedPoints = sorted(allPoints,
                          key = lambda point: (point[0], point[1]))

    # add the tuples into a set, if it's (x+-10, y+-10) is not already inside
    # by default, bounds is 10

    # dedupe sorted tuples in sortedPoints list
    deduped = [] # deduped list of tuples

    # add first tuple
    deduped.append(sortedPoints[0]) 

    setY = set([])
    # add first element's range of y values
    for i in range((2*bounds+1)+1):
        setY.add(sortedPoints[0][1] - bounds + i)

    for i in range(1,len(sortedPoints)):

        point = sortedPoints[i]
        prev = sortedPoints[i-1]
        
        x, y = point[0], point[1]
        prevX, prevY = prev[0], prev[1]

        if not (prevX-bounds <= x <= prevX+bounds):
            deduped.append(point)
            setY = set([]) # reset set of y-value ranges
                
        else: # x is within the range of +- bounds
            # deciding whether to add the whole coordinate or not
            if y not in setY:
                deduped.append(point)
                
        for j in range((2*bounds+1)+1):
            # add the +- 2 range of values into the set
            fuzzY = y - bounds + j
            setY.add(fuzzY)
##
##    for point in deduped:
##        print(point)
        
    return deduped
##        r = 10
##    
##        cv2.circle(scoreImage, (point[0] + r, point[1] +r), r, rgb, 2)
##    print(len(deduped))



def locations(imageFile, scoreFile, musicType=('n',1,4),
              color=1, threshold=0.885):
    # returns the locations of the png 'imageFile' in the png 'score'
    # color=1 (color), color=0 (grayscale), color=-1 (unchanged)
    # threshold of 0.885 match has been empirically tested

    img = cv2.imread(imageFile, color)
    scoreImg = cv2.imread(scoreFile, color)
    # takes in scoreImage for now
    

    # using openCV to match img on scoreImg, match coordinates are top
    # left corner of each img template
    result = cv2.matchTemplate(scoreImg, img, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)

    # converting numpy array to list of tuples of note coordinates
    allPoints = []
    for point in zip(*location[::-1]):
        allPoints.append((point[0], point[1], musicType))
        
    deduped = deduplicate(allPoints)
    
    return deduped

# the final idea
location = locations('./MusicNotesTemplate/semibreveLine.png',
                     './MusicScores/Sample1.png')


scoreImg = cv2.imread('./MusicScores/Sample1.png', 1)
print(location)
for point in location:
    r = 10
    cv2.circle(scoreImg, (point[0], point[1]), r,
               (0,0,255), 2)
    
print(len(location))

cv2.imshow('score display',scoreImg)

# waits for any keystroke to continue to destroy all windows
cv2.waitKey(0) 
cv2.destroyAllWindows() 
    
'''
def drawLocations(imageFile, scoreImage, color=1, threshold=0.855,rgb=(0,0,255)):
    # function to draw locations of identified notes, for checking purposes

    location = locations(imageFile, scoreImage)
    #scoreImage = cv2.imread(score, color)
    # let the function take in the actual image object for now
   

    # converting numpy array to list of tuples of note coordinates
    allPoints = []
    for point in zip(*location[::-1]):
        allPoints.append(point)

    # sort the tuples based on x and y coordinates
    sortedPoints = sorted(allPoints,
                       key = lambda point: (point[0], point[1]))

    # add the tuples into a set, if it's (x+-2, y+-2) is not already inside
    #sorted(unsorted, key=lambda element: (element[1], element[2]))

    # dedupe sorted tuples
    
    deduped = [] # another list of tuples
    
    deduped.append(sortedPoints[0]) # add first element


    setY = set([])
    # add first element's range of y values
    bounds = 2 # plus minus 2
    for i in range((2*bounds+1)+1):
        setY.add(sortedPoints[0][1] - bounds + i)

    for i in range(1,len(sortedPoints)):

        point = sortedPoints[i]
        prev = sortedPoints[i-1]
        
        x, y = point
        prevX, prevY = prev
        
        bounds = 10 # plus minus 2

        if not (prevX-bounds <= x <= prevX+bounds):
            deduped.append(point)
            setY = set([]) # reset set of y-values
                
            
        else: # x is within the range of +- bounds
            # deciding whether to add the coordinate or not
            if y not in setY:
                deduped.append(point)
                
        for j in range((2*bounds+1)+1):
            # add the +- 2 range of values into the set
            fuzzY = y - bounds + j
            setY.add(fuzzY)

    for point in deduped:
        #print(point)
        r = 10
    
        cv2.circle(scoreImage, (point[0] + r, point[1] +r), r, rgb, 2)
    print(len(deduped))
    
#drawLocations('./MusicNotesTemplate/minimLine.png',
#              './MusicScores/Sample1.png')

def drawAll(score,color=1):
    # takes in score as string
    # draws the whole thing in the end
    scoreImage = cv2.imread(score, color)
    drawLocations('./MusicNotesTemplate/semibreveRest.png',
                  scoreImage)

##    for point in [(200, 414), (334, 674)]:
##        r = 10
##        cv2.circle(scoreImage, (point[0] + r, point[1] +r), r, (0,255,0), 2)
##    
    cv2.imshow('score display',scoreImage)

    # waits for any keystroke to continue to destroy all windows
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 

drawAll('./MusicScores/Sample1.png')
'''
