from cv2 import imread, imwrite, imshow, IMREAD_GRAYSCALE, namedWindow, waitKey, destroyAllWindows
import numpy as np


def morph_erode(img):
    #creating the structuring element
    b = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]]).astype(int)

    #zero-padding the image to retain the size after erosion
    im = np.pad(img,((1,1),(1,1)),'constant')

    #initializing erosion output array
    erode_img = np.zeros((np.shape(im)[0],np.shape(im)[1]))

    #replacing image array with 0s and 1s
    im = im / 255

    #erosion operation
    for i in range(0, np.shape(im)[0]-1):
        for j in range(0, np.shape(im)[1]-1):

            #slicing a part of the input image to match the size of the structuring element
            k = im[i:i + np.shape(b)[0], j:j + np.shape(b)[1]] 
            if np.array_equal(k, b):
                erode_img[i + 1][j + 1] = 255
            else:
                erode_img[i + 1][j + 1] = 0
    
    #removing zero-padding before returning erosion output
    erode_img = erode_img[1:-1, 1:-1]
    
    return erode_img


def morph_dilate(img):
    #creating the structuring element
    b = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]]).astype(int)

    #zero-padding the image to retain the size after erosion
    im = np.pad(img,((1,1),(1,1)),'constant')

    #initializing erosion output array
    dilate_img = np.zeros((np.shape(im)[0],np.shape(im)[1]))

    #replacing image array with 0s and 1s
    im = im / 255

    #dilation operation
    for i in range(0, np.shape(im)[0] - 2):
        for j in range(0, np.shape(im)[1] - 2):
            
            #slicing a part of the input image to match the size of the structuring element
            k = im[i:i + np.shape(b)[0], j:j + np.shape(b)[1]]
            if np.sometrue(np.equal(k, b)):
                dilate_img[i + 1][j + 1] = 255
            else:
                dilate_img[i + 1][j + 1] = 0
    
    #removing zero-padding before returning erosion output
    dilate_img = dilate_img[1:-1, 1:-1]
    
    return dilate_img


def morph_open(img):
    open_img = morph_dilate(morph_erode(img))

    return open_img


def morph_close(img):
    close_img = morph_erode(morph_dilate(img))

    return close_img


def denoise(img):
    denoise_img = morph_close(morph_open(img))

    return denoise_img


def boundary(img):
    bound_img = np.subtract(img, morph_erode(img))

    return bound_img


if __name__ == "__main__":
    img = imread('task3.png', IMREAD_GRAYSCALE)
    denoise_img = denoise(img)
    imwrite('results/task3_denoise.jpg', denoise_img)
    bound_img = boundary(denoise_img)
    imwrite('results/task3_boundary.jpg', bound_img)





