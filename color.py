import cv2
import numpy as np
import pandas as pd
import argparse

# 명령 줄에서 이미지 경로를 가져오기 위한 인수 파서 생성
ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image', required=True, help="Image Path")
ap.add_argument('--image', default='/color_detection/colorpic.jpg', type=str, dest='image', required=False, help="이미지 경로")
args = vars(ap.parse_args())
img_path = args['image']

# opencv를 사용하여 이미지 읽기
img = cv2.imread(img_path)

# 전역 변수 선언 (나중에 사용됨)
clicked = False
r = g = b = xpos = ypos = 0

# pandas를 사용하여 csv 파일 읽기 및 각 열에 이름 지정
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('color_detection/colors.csv', names=index, header=None)

# 모든 색상으로부터 최소 거리를 계산하고 가장 일치하는 색상을 얻는 함수
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# 마우스 더블 클릭의 x,y 좌표를 얻는 함수
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
    
cv2.destroyAllWindows()

