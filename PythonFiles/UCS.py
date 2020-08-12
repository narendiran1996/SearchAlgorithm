import cv2
import os
import numpy as np
import collections
dictll ={'Nilgiris': (607, 134), 'Coimbatore': (539, 178), 'Tiruppur': (553, 245), 'Erode': (590, 304), 'Dindigul': (423, 350), 'Theni': (372, 267), 'Madurai': (356, 366), 'Virudunagar': (279, 343), 'Ramanathapuram': (254, 489), 'Tenkasi': (189, 234), 'Tirunelveli': (152, 302), 'Kanyakumari': (53, 254), 'Thoothukudi': (154, 373), 'Sivagangai': (335, 438), 'Pudukottai': (426, 493), 'Trichy': (493, 469), 'Perambalur': (572, 504), 'Ariyalur': (550, 535), 'Tanjavur': (495, 543), 'Tiruvarur': (494, 623), 'Cuddalore': (660, 646), 'Villupuram': (695, 600), 'Kallakurichi': (652, 509), 'Namakkal': (572, 379), 'Karur': (524, 364), 'Salem': (647, 381), 'Chengalpattu': (819, 682), 'Chennai': (885, 729), 'Tiruvallur': (898, 671), 'Tiruvannamalai': (742, 534), 'Dharmapuri': (725, 377), 'Krishnagiri': (793, 388), 'Vellore': (862, 576), 'Nagapattinam': (495, 658),'Pondicherry': (679, 651) }

font = cv2.FONT_HERSHEY_SIMPLEX
nodeDict = {}

class Nodedetail:
    def __init__(self,name):
        self.name = name
        self.neighbourNodeDict = {}
    def addNeighbour(self, neighbourNode, distance):
        self.neighbourNodeDict[neighbourNode.name] = distance
    def getNeighboursLexi(self):
        sorted_x = sorted(self.neighbourNodeDict.items(), key=lambda kv: kv[0])
        return collections.OrderedDict(sorted_x)
    def getNeighboursDist(self):
        sorted_x = sorted(self.neighbourNodeDict.items(), key=lambda kv: kv[1])
        return collections.OrderedDict(sorted_x)
    def __str__(self):
        st = 'My name is '+self.name+' and my neighbours are\n'
        # for k,v in self.getNeighboursLexi().items():
        #     st = st + k + ' : ' + str(v) + '\n'
        return st
    def __repr__(self):
        return self.name


img = cv2.imread('../tamilNaduOutline.jpg')

def drawNodeColor(nimg, pointP, color):
    p = pointP
    overlay = nimg.copy()
    alpha = 0.6
    
    if color == 'white':
        cv2.circle(overlay, p, 10, (0, 0, 0), 1)
        return overlay
    elif color == 'blue':
        cv2.circle(overlay, p, 10, (215, 173, 0), -1)
        return cv2.addWeighted(overlay, alpha, nimg, 1 - alpha, 0)
    elif color == 'orange':
        cv2.circle(overlay, p, 10, (8, 121, 243), -1)
        return cv2.addWeighted(overlay, alpha, nimg, 1 - alpha, 0)
    elif color == 'gray':
        cv2.circle(overlay, p, 10, (172, 172, 172), -1)
        return cv2.addWeighted(overlay, alpha, nimg, 1 - alpha, 0)
    elif color == 'black':
        cv2.circle(overlay, p, 10, (0, 0, 0), -1)
        return overlay
    elif color == 'green':
        cv2.circle(overlay, p, 10, (0, 255, 0), -1)
        return cv2.addWeighted(overlay, alpha, nimg, 1 - alpha, 0)
def drawPoints():
    img = cv2.imread('../tamilNadu2.jpg') 
    print(img.shape)
    emptyImg = np.ones((cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)).shape)*255.0

    for district, points in dictll.items():
        cv2.circle(emptyImg, points, 3, (0,0,0), -1)
        emptyImg = drawNodeColor(emptyImg, points, 'gray')
        gunda = np.zeros((emptyImg.shape))
        gunda = cv2.rotate(gunda, cv2.ROTATE_90_COUNTERCLOCKWISE)
        newNode = Nodedetail(district)
        nodeDict[district] = newNode
        cv2.putText(gunda, district, (points[1]+5,1000-points[0]-5), font, 0.3, (0,255,255), 1)
        gunda = cv2.rotate(gunda, cv2.ROTATE_90_CLOCKWISE)
        emptyImg = emptyImg - gunda
    # cv2.imwrite('tamilNaduOutline.jpg', cv2.rotate(emptyImg, cv2.ROTATE_90_COUNTERCLOCKWISE))
    cv2.imwrite('../tamilNaduOutline.jpg', emptyImg)

drawPoints()



def plotPath(img, key1, key2, dist):
    n1 = nodeDict[key1]
    n2 = nodeDict[key2]
    n1.addNeighbour(n2, dist)
    n2.addNeighbour(n1, dist)
    cv2.line(img, dictll[key1], dictll[key2], (0,0,0),1)
    p1 = tuple(map(lambda x, y: int((x + y)/2), dictll[key1], dictll[key2]))
    cv2.putText(img, str(dist) , p1, font, 0.25, (0,0,255))
    return img

img = plotPath(img, 'Nilgiris', 'Coimbatore', 100)
img = plotPath(img, 'Coimbatore', 'Tiruppur', 55)
img = plotPath(img, 'Coimbatore', 'Erode', 99)
img = plotPath(img, 'Coimbatore', 'Dindigul', 154)
img = plotPath(img, 'Theni', 'Dindigul', 75)
img = plotPath(img, 'Theni', 'Madurai', 75)
img = plotPath(img, 'Karur', 'Coimbatore', 130)
img = plotPath(img, 'Salem', 'Erode', 64)
img = plotPath(img, 'Karur', 'Dindigul', 78)
img = plotPath(img, 'Erode', 'Tiruppur', 57)
img = plotPath(img, 'Salem', 'Dharmapuri', 67)
img = plotPath(img, 'Karur', 'Namakkal', 34)
img = plotPath(img, 'Salem', 'Namakkal', 52)
img = plotPath(img, 'Madurai', 'Dindigul', 63)
img = plotPath(img, 'Krishnagiri', 'Dharmapuri', 282)
img = plotPath(img, 'Krishnagiri', 'Vellore', 119)
img = plotPath(img, 'Tiruvannamalai', 'Vellore', 83)
img = plotPath(img, 'Chennai', 'Vellore', 137)
img = plotPath(img, 'Chennai', 'Chengalpattu', 62)
img = plotPath(img, 'Chengalpattu', 'Vellore', 111)
img = plotPath(img, 'Chennai', 'Tiruvallur', 39)
img = plotPath(img, 'Chengalpattu', 'Villupuram', 105)
img = plotPath(img, 'Tiruvannamalai', 'Krishnagiri', 112)
img = plotPath(img, 'Tiruvannamalai', 'Villupuram', 61)
img = plotPath(img, 'Cuddalore', 'Villupuram', 44)
img = plotPath(img, 'Cuddalore', 'Chengalpattu', 127)
img = plotPath(img, 'Cuddalore', 'Nagapattinam', 131)
img = plotPath(img, 'Tiruvarur', 'Nagapattinam', 27)
img = plotPath(img, 'Tiruvarur', 'Tanjavur', 61)
img = plotPath(img, 'Salem', 'Villupuram', 181)
img = plotPath(img, 'Salem', 'Cuddalore', 199)
img = plotPath(img, 'Ariyalur', 'Cuddalore', 157)
img = plotPath(img, 'Perambalur', 'Cuddalore', 130)
img = plotPath(img, 'Villupuram', 'Perambalur', 109)

img = plotPath(img, 'Villupuram', 'Tanjavur', 176)
img = plotPath(img, 'Tanjavur', 'Ariyalur', 44)
img = plotPath(img, 'Perambalur', 'Tanjavur', 72)
img = plotPath(img, 'Tanjavur', 'Trichy', 59)
img = plotPath(img, 'Tanjavur', 'Pudukottai', 62)

img = plotPath(img, 'Trichy', 'Pudukottai', 52)
img = plotPath(img, 'Trichy', 'Karur', 82)
img = plotPath(img, 'Trichy', 'Dindigul', 101)
img = plotPath(img, 'Trichy', 'Madurai', 135)

img = plotPath(img, 'Sivagangai', 'Pudukottai', 81)
img = plotPath(img, 'Ramanathapuram', 'Pudukottai', 129)
img = plotPath(img, 'Ramanathapuram', 'Nagapattinam', 214)


img = plotPath(img, 'Sivagangai', 'Madurai', 45)
img = plotPath(img, 'Sivagangai', 'Ramanathapuram', 86)
img = plotPath(img, 'Madurai', 'Ramanathapuram', 115)

img = plotPath(img, 'Madurai', 'Thoothukudi', 147)
img = plotPath(img, 'Madurai', 'Virudunagar', 57)
img = plotPath(img, 'Madurai', 'Tenkasi', 161)
img = plotPath(img, 'Madurai', 'Tirunelveli', 161)

img = plotPath(img, 'Tirunelveli', 'Thoothukudi', 49)
img = plotPath(img, 'Tirunelveli', 'Virudunagar', 109)
img = plotPath(img, 'Tirunelveli', 'Thoothukudi', 46)
img = plotPath(img, 'Tirunelveli', 'Kanyakumari', 85)
img = plotPath(img, 'Tenkasi', 'Kanyakumari', 130)


img = plotPath(img, 'Pondicherry', 'Cuddalore', 22)
img = plotPath(img, 'Pondicherry', 'Chennai', 175)
img = plotPath(img, 'Pondicherry', 'Chengalpattu', 105)
img = plotPath(img, 'Pondicherry', 'Villupuram', 39)

import math
dicDistanceFromSource = {}
def distanceBetweenNodes(fromNode, parent, node1):
    global dicDistanceFromSource 
    sourceNode = nodeDict[fromNode]
    parentNode = nodeDict[parent]
    childNode = nodeDict[node1]


    
    NodeDistanceFromParent = 0

    if parent not in dicDistanceFromSource.keys():
        if parent in sourceNode.neighbourNodeDict.keys():
            dicDistanceFromSource[parent] = sourceNode.neighbourNodeDict[parent]
        else:
            dicDistanceFromSource[parent] = 0
    else:
        if node1 not in dicDistanceFromSource.keys():
            if node1 in parentNode.neighbourNodeDict.keys():
                NodeDistanceFromParent = parentNode.neighbourNodeDict[node1]
            else:
                NodeDistanceFromParent = 0
               
    dicDistanceFromSource[node1] = NodeDistanceFromParent + dicDistanceFromSource[parent]


# print(nodeDict['Coimbatore'])
class MyPrioirtyQueue():
    def __init__(self):
        self.myQueue = []
    def enqueue(self,  valu):
        self.myQueue.append(valu)
    def dequeue(self):
        minDistanceIndex = 0
        for i in range(len(self.myQueue)):
            if dicDistanceFromSource[self.myQueue[i]] < dicDistanceFromSource[self.myQueue[minDistanceIndex]]:
                minDistanceIndex = i
        minDistanceElement = self.myQueue[minDistanceIndex]
        del self.myQueue[minDistanceIndex]
        return minDistanceElement
    def isEmpty(self):
        return len(self.myQueue) == 0

def dispKey(img):
    cv2.imshow('TestImage', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def amIover(nodeName, explored):
    for nnn in list(nodeDict[nodeName].neighbourNodeDict.keys()):
        if nnn not in explored:
            return False
    return True

cv2.namedWindow('TestImage',cv2.WINDOW_NORMAL)
cv2.resizeWindow('TestImage', 800,640)
def UCS(fromNode, toNode):
    if os.path.exists('../UCSoutput/'):
        import shutil
        shutil.rmtree('../UCSoutput/')
    os.makedirs('../UCSoutput/')
    global img, dicDistanceFromSource
    dicDistanceFromSource[fromNode] = 0
    frontier = MyPrioirtyQueue()
    frontier.enqueue(fromNode)    
    explored = []
    img = drawNodeColor(img, dictll[fromNode], 'blue')
    i=0
    cv2.imwrite('../UCSoutput/tamilUCS'+str(i)+'.jpg', cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    i = i + 1
    while frontier.isEmpty() == False: 
     
        currentNode = frontier.dequeue()
        explored.append(currentNode)
        if currentNode == toNode:
            print(i)
            img = drawNodeColor(img, dictll[toNode], 'green')   
            cv2.imwrite('../UCSoutput/tamilUCS'+str(i)+'.jpg', cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            return explored
        
        
        img = drawNodeColor(img, dictll[currentNode], 'orange')
        stat = 0
        for neigh in nodeDict[currentNode].getNeighboursLexi():
            if neigh not in (frontier.myQueue + explored):
                stat=1
                frontier.enqueue(neigh)
                img = drawNodeColor(img, dictll[neigh], 'blue')
                distanceBetweenNodes(fromNode, currentNode, neigh)
                print(currentNode,' Ghost ; ', neigh)

        cv2.imwrite('../UCSoutput/tamilUCS'+str(i)+'.jpg', cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
        i = i + 1
        print('[',end='')
        for k in range(len(frontier.myQueue)):
            print("'"+frontier.myQueue[k]+"'"+' - '+str(dicDistanceFromSource[frontier.myQueue[k]]), end=',')
        print(']')
        if stat==0:
            print('black repeat')
            img = drawNodeColor(img, dictll[currentNode], 'black')
            cv2.imwrite('../UCSoutput/tamilUCS'+str(i)+'.jpg', cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            i = i + 1
        # print(dicDistanceFromSource)
        # cv2.imshow('TestImage', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
print(UCS('Coimbatore', 'Pondicherry'))
print(dicDistanceFromSource)
