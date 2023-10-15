import numpy as np
import cv2 as cv
import glob
# 终止条件
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# 准备对象点， 如 (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((10*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:10].T.reshape(-1,2)
# 用于存储所有图像的对象点和图像点的数组。
objpoints = [] # 真实世界中的3d点
imgpoints = [] # 图像中的2d点
images = glob.glob('./imgset(1)/*.jpg')
# print(images)

for fname in images:
    img = cv.imread(fname)

    cv.namedWindow('img', cv.WINDOW_NORMAL)
    # cv.imshow('img', img)
    # cv.waitKey(0)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 找到棋盘角落
    ret, corners = cv.findChessboardCorners(gray, (7, 10), None)

    a = 1
    # 如果找到，添加对象点，图像点（细化之后）
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # 绘制并显示拐角
        cv.drawChessboardCorners(img, (7, 10), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread('./imgset(1)/b07a0a95324dbfae66a8c02543e753e.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))


 # undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
cv.imwrite('calibresult.png', dst)

# # 剪裁图像
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# cv.imwrite('calibresult.png', dst)




# # undistort
# mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
# dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
# # 裁剪图像
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# cv.imwrite('calibresult.png', dst)
#
#
# mean_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
#     mean_error += error
# print( "total error: {}".format(mean_error/len(objpoints)) )