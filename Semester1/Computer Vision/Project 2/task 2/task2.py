"""
 Grayscale Image Processing
(Due date: Nov. 26, 11:59 P.M., 2021)

The goal of this task is to experiment with two commonly used 
image processing techniques: image denoising and edge detection. 
Specifically, you are given a grayscale image with salt-and-pepper noise, 
which is named 'task2.png' for your code testing. 
Note that different image might be used when grading your code. 

You are required to write programs to: 
(i) denoise the image using 3x3 median filter;
(ii) detect edges in the denoised image along both x and y directions using Sobel operators (provided in line 30-32).
(iii) design two 3x3 kernels and detect edges in the denoised image along both 45° and 135° diagonal directions.
Hint: 
• Zero-padding is needed before filtering or convolution. 
• Normalization is needed before saving edge images. You can normalize image using the following equation:
    normalized_img = 255 * frac{img - min(img)}{max(img) - min(img)}

Do NOT modify the code provided to you.
You are NOT allowed to use OpenCV library except the functions we already been imported from cv2. 
You are allowed to use Numpy for basic matrix calculations EXCEPT any function/operation related to convolution or correlation. 
You should NOT use any other libraries, which provide APIs for convolution/correlation ormedian filtering. 
Please write the convolution code ON YOUR OWN. 
"""

from cv2 import imread, imwrite, imshow, IMREAD_GRAYSCALE, namedWindow, waitKey, destroyAllWindows
import numpy as np
import statistics

# Sobel operators are given here, do NOT modify them.
sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]).astype(int)
sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]).astype(int)
diag_45 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]).astype(int)
diag_135 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]).astype(int)

def filter(img):
    """
    :param img: numpy.ndarray(int), image
    :return denoise_img: numpy.ndarray(int), image, same size as the input image

    Apply 3x3 Median Filter and reduce salt-and-pepper noises in the input noise image
    """
    
    #zero-padding
    im = np.pad(img,((1,1),(1,1)),'constant')
    for i in range(1,np.shape(im)[0]-2):
        for j in range(1,np.shape(im)[1]-2):
            im[i][j] = statistics.median([im[i-1][j-1],im[i-1][j],im[i-1][j+1],im[i][j-1],im[i][j],im[i][j+1],im[i+1][j-1],im[i+1][j],im[i+1][j+1]])
    
    denoise_img = im[1:-1,1:-1]
    return denoise_img

def convolve2d(img, kernel):
    """
    :param img: numpy.ndarray, image
    :param kernel: numpy.ndarray, kernel
    :return conv_img: numpy.ndarray, image, same size as the input image

    Convolves a given image (or matrix) and a given kernel.
    """
    #zero-padding
    im = np.pad(img,((1,1),(1,1)),'constant')
    
    #flipping the kernel for convolution
    K = np.flip(kernel,0)
    k = np.flip(K,1)
    
    #initializing convolution output array with image dimensions
    conv_img = np.zeros((np.shape(im)[0],np.shape(im)[1]))

    #convoluting with the kernel to get the convolution output
    for i in range(1,np.shape(conv_img)[0]-1):
        for j in range(1,np.shape(conv_img)[1]-1):
            conv_img[i][j] = (im[i-1][j-1]*k[0][0]+im[i-1][j]*k[0][1]+im[i-1][j+1]*k[0][2]+im[i][j-1]*k[1][0]+im[i][j]*k[1][1]+im[i][j+1]*k[1][2]+im[i+1][j-1]*k[2][0]+im[i+1][j]*k[2][1]+im[i+1][j+1]*k[2][2])
    
    #removing padding
    conv_img = conv_img[1:-1,1:-1]
    return conv_img


def edge_detect(img):
    """
    :param img: numpy.ndarray(int), image
    :return edge_x: numpy.ndarray(int), image, same size as the input image, edges along x direction
    :return edge_y: numpy.ndarray(int), image, same size as the input image, edges along y direction
    :return edge_mag: numpy.ndarray(int), image, same size as the input image, 
                      magnitude of edges by combining edges along two orthogonal directions.

    Detect edges using Sobel kernel along x and y directions.
    Please use the Sobel operators provided in line 30-32.
    Calculate magnitude of edges by combining edges along two orthogonal directions.
    All returned images should be normalized to [0, 255].
    """
    edge_x = convolve2d(img,sobel_x)
    edge_y = convolve2d(img,sobel_y)
    edge_mag = np.sqrt(np.square(edge_x)+np.square(edge_y))
    
    #normalizing the output
    x_min = edge_x.min()
    x_max = edge_x.max()
    y_min = edge_y.min()
    y_max = edge_y.max()
    m_max = edge_mag.max()
    m_min = edge_mag.min()
    for x in edge_x:
        x = 255 * (x - x_min)/(x_max - x_min)
    for y in edge_y:
        y = 255 * (y - y_min)/(y_max - y_min)
    for m in edge_mag:
        m = 255 * (m - m_min)/(m_max - m_min)

    edge_x = np.array(edge_x).astype(int)
    edge_y = np.array(edge_y).astype(int)
    edge_mag = np.array(edge_mag).astype(int)

    return edge_x, edge_y, edge_mag


def edge_diag(img):
    """
    :param img: numpy.ndarray(int), image
    :return edge_45: numpy.ndarray(int), image, same size as the input image, edges along x direction
    :return edge_135: numpy.ndarray(int), image, same size as the input image, edges along y direction

    Design two 3x3 kernels to detect the diagonal edges of input image. Please print out the kernels you designed.
    Detect diagonal edges along 45° and 135° diagonal directions using the kernels you designed.
    All returned images should be normalized to [0, 255].
    """
    edge_45 = convolve2d(img,diag_45)
    edge_135= convolve2d(img,diag_135)
    
    #normalizing the output
    d1_min = edge_45.min()
    d1_max = edge_45.max()
    d2_min = edge_135.min()
    d2_max = edge_135.max()
    for x in edge_45:
        x = 255 * (x - d1_min)/(d1_max - d1_min)
    for y in edge_135:
        y = 255 * (y - d2_min)/(d2_max - d2_min)
    
    edge_45 = np.array(edge_45).astype(int)
    edge_135 = np.array(edge_135).astype(int)

    #the two diagonal kernels designed 
    print("Diagonal edge filter along 45 degrees:", diag_45,"\n")
    print("Diagonal edge filter along 135 degrees:", diag_135,"\n") 
    return edge_45, edge_135


if __name__ == "__main__":
    noise_img = imread('task2.png', IMREAD_GRAYSCALE)
    denoise_img = filter(noise_img)
    imwrite('results/task2_denoise.jpg', denoise_img)
    edge_x_img, edge_y_img, edge_mag_img = edge_detect(denoise_img)
    imwrite('results/task2_edge_x.jpg', edge_x_img)
    imwrite('results/task2_edge_y.jpg', edge_y_img)
    imwrite('results/task2_edge_mag.jpg', edge_mag_img)
    edge_45_img, edge_135_img = edge_diag(denoise_img)
    imwrite('results/task2_edge_diag1.jpg', edge_45_img)
    imwrite('results/task2_edge_diag2.jpg', edge_135_img)





