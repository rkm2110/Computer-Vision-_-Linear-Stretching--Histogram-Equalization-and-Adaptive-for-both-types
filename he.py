import cv2
import numpy as np
import sys

# read arguments
if len(sys.argv) != 3:
    print(sys.argv[0], ": takes 2 arguments. Not ", len(sys.argv) - 1)
    print("Expecting argument: Input image name and output image name.")
    print("Example:", sys.argv[0], "inputimage outputimage")
    sys.exit()

name_input = sys.argv[1]
name_output = sys.argv[2]

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

# Histogram Equalization
HE_L = cv2.equalizeHist((L_values))

# Set L values back to the LUV image
LUV_image[:, :, 0] = HE_L

# LUV to BGR
outputImage = cv2.cvtColor(LUV_image, cv2.COLOR_LUV2BGR)

# Display output image
cv2.imshow("Output Image: " + name_output, outputImage)

# Write the output image
cv2.imwrite(name_output, outputImage)

# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
