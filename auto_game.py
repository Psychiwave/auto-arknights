# -*- coding:utf-8 -*-
# @author：LuffyLSX
# @version：1.0
# @update time：2019/8/31

import os,time
import cv2
import timeit

# adbExe = '%LOCALAPPDATA%\\Android\\sdk\\platform-tools\\adb.exe' #adb position

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def start_app():
    try:
        os.system('adb shell am start -n com.hypergryph.arknights/com.u8.sdk.U8UnityContext')  #启动arknights app（用'dumpsys activity top | grep ACTIVITY' 查看当前的activity 
    except:
        print('启动失败')

def click(x, y):
    os.system('adb shell input tap %s %s' % (x, y)) #点击位置(x,y)

def screenshot():
    path = os.path.abspath('.') + '\images'
    os.system('adb shell screencap /sdcard/Documents/screen.png')  #截图并保存到。。。
    os.system('adb pull /sdcard/Documents/screen.png %s' % path)  #拉下来到本地

def resize_img(img_path):
    img1 = cv2.imread(img_path, 0)  #读预先存好的照片
    img2 = cv2.imread('images/screen.png', 0)  #读刚截图的照片
    height, width = img1.shape[:2]  #获取图片分辨率（长、宽
    ratio = 2560 / img2.shape[1]    
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation = cv2.INTER_AREA)

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image) + '.png'
    screen = cv2.imread('images/screen.png', 0)
    # template = cv2.imread(image_path, 0)
    template = resize_img(image_path)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print(max_val)
    if max_val > 0.8:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        print(center)
        return center
    else:
        return False
    
def run(n):
    run.start = timeit.default_timer() #开始时间
    images = ['start-go1', 'start-go2', 'end', 'level up']
    round = 0
    # Image_to_position('start-go1')
    # time.sleep(2)
    # Image_to_position('start-go2')
    # while not Image_to_position('end'):
    #     time.sleep(5) 
    while True:
        screenshot()
        now = ''
        for image in images:
            if Image_to_position(image, m = 0) != False:
                print(image)
                now = image
                time.sleep(0.5)
                click(center[0], center[1])
        if now == 'start-go2':
            print('第%s次开始' % (round + 1))
            print('进度：%s/%s' % (round + 1, n))            
        if now == 'end':
            time.sleep(1)
            print('第%s次结束' % (round + 1))  
            round = round + 1 
            if round == n:
                break
        
def usetime():
    end = timeit.default_timer()
    totaltime = round(end - run.start, 3)
    m, s = divmod(totaltime, 60)
    print("一共用时%d分%s秒" % (m, round(s, 2)))


if __name__ == '__main__':
    # connect()
    start_app()
    '''for i in range(int(input('输入刷图次数' + '\n'))):
        run()
        time.sleep(3)'''
    
    run(int(input('输入刷图次数' + '\n')))
    os.system('adb kill-server')
    usetime()

