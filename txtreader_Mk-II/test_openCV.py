import cv2

img = "/Users/matsuurakenshin/WorkSpace/development/txtreader/sample_image.jpeg"
img = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',img)

cv2.waitKey(0)
cv2.destroyAllWindows() 