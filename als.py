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

# Keep a copy of original L values
new_L_values = L_values.copy()

for i in range(0, len(L_values)):
    for j in range(0, len(L_values[i])):

        # Get minimum value
        if i - w < 0 or j - w < 0 or i + w >= len(L_values) or j + w >= len(L_values[0]):
            min_value = 0
        else:
            min_value = L_values[i - w][j - w]
            for k in range(i - w, i + w + 1):
                for l in range(j - w, j + w + 1):
                    min_value = min(min_value, L_values[k][l])

        # Get maximum value
        max_value = L_values[0][0]
        for k in range(max(0, i - w), min(i + w, len(L_values) - 1) + 1):
            for l in range(max(0, j - w), min(j + w, len(L_values[0]) - 1) + 1):
                max_value = max(max_value, L_values[k][l])

        new_L_values[i][j] = 255 * ((L_values[i][j] - min_value) / (max_value - min_value))


# Set L values back to the LUV image
LUV_image[:, :, 0] = new_L_values

# LUV to BGR
outputImage = cv2.cvtColor(LUV_image, cv2.COLOR_LUV2BGR)

# Display output image
cv2.imshow("Output Image: " + name_output, outputImage)

# Write the output image
cv2.imwrite(name_output, outputImage)

# wait for key to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
