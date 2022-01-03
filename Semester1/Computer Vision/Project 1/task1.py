###############
##Design the function "findRotMat" to  return 
# 1) rotMat1: a 2D numpy array which indicates the rotation matrix from xyz to XYZ 
# 2) rotMat2: a 2D numpy array which indicates the rotation matrix from XYZ to xyz 
#It is ok to add other functions if you need
###############

import numpy as np
import cv2

def findRotMat(alpha, beta, gamma):
    #......
    a=np.radians(alpha)
    b=np.radians(beta)
    g=np.radians(gamma)
    
    m1=np.array([np.cos(a),-np.sin(a),0,np.sin(a),np.cos(a),0,0,0,1]).reshape(3,3)
    m2=np.array([1,0,0,0,np.cos(b),-np.sin(b),0,np.sin(b),np.cos(b)]).reshape(3,3)
    m3=np.array([np.cos(g),-np.sin(g),0,np.sin(g),np.cos(g),0,0,0,1]).reshape(3,3)
    
    R=np.dot(m3,(np.dot(m2,m1)))
    R_Inv=np.linalg.inv(R)
    return R,R_Inv


if __name__ == "__main__":
    alpha = 45
    beta = 30
    gamma = 60
    rotMat1, rotMat2 = findRotMat(alpha, beta, gamma)
    print(rotMat1)
    print(rotMat2)
