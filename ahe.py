import cv2
import numpy as np
import sys

# read arguments
if len(sys.argv) != 4:
    print(sys.argv[0], ": takes 3 arguments. Not ", len(sys.argv) - 1)
    print("Expecting argument: input image name, window parameter(w) and output image name.")
    print("Example:", sys.argv[0], "w inputimage outputimage")
    print("Example:", sys.argv[0], "20 fruits.jpg out.jpg")
    sys.exit()

w = int(sys.argv[1])
name_input = sys.argv[2]
name_output = sys.argv[3]

# read image
inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
if inputImage is None:
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

rows, cols, bands = inputImage.shape
if bands != 3:
    print("Input image is not a standard color image:", inputImage)
    sys.exit()

# Display input image
cv2.imshow("Input Image: " + name_input, inputImage)

# BGR to LUV
LUV_image = cv2.cvtColor(inputImage, cv2.COLOR_BGR2LUV)

# Get the L values : (a 2D matrix)
L_values = LUV_image[:, :, 0]

#Use open CV to use Adaptive Histogram Equalization
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(w, w))
equalized = clahe.apply(L_values)


# Set L values back to the LUV image
LUV_image[:, :, 0] = equalized

# LUV to BGR
outputImage = cv2.cvtColor(LUV_image, cv2.COLOR_LUV2BGR)

# Display output image
cv2.imshow("Output Image: " + name_output, outputImage)

# Write the output image
cv2.imwrite(name_output, outputImage)

# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
