"""
Createb by DucVM
"""
from  __future__ import print_function
from  __future__ import division
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os


# def function load array diffirences of all frame in video and show
def load_and_show_histogram(inputfolder, type):
    if type == "hsv":
        rsvfile = inputfolder + "/hsv.txt"
        arr_diff = np.loadtxt(rsvfile, dtype=np.float, delimiter="\n")
        plt.plot(arr_diff, color='r')
        plt.ylabel('distance')
        plt.show()
    else:
        hog_file = inputfolder + "/rog.txt"
        arr_diff = np.loadtxt(hog_file, dtype=np.float, delimiter="\n")
        plt.plot(arr_diff, color='r')
        plt.ylabel('distance')
        plt.show()
    cv2.destroyAllWindows()


# def function to calculating the constrast of gray image
def calConstrastGray(img_gray):
    var = np.var(img_gray)
    mean = np.mean(img_gray)
    height, width = img_gray.shape
    size = height * width
    constrast = np.sqrt(1 / size * np.sum((img_gray - mean) * (img_gray - mean)))
    return constrast


# def function to calculating the constrast of color image
def calConstrastColor(img_gray):
    var = np.var(img_gray)
    mean = np.mean(img_gray)
    height, width, chanel = img_gray.shape
    size = height * width
    constrast = np.sqrt(1 / size * np.sum((img_gray - mean) * (img_gray - mean)))
    return constrast


# concat many frame to one
def concat_shot(arr_uri_shot, uri_out):
    # read
    cap0 = cv2.VideoCapture(arr_uri_shot[0])
    fps = int(cap0.get(cv2.CAP_PROP_FPS))
    width = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(uri_out, fourcc, fps, (width, height))
    length_shot = len(arr_uri_shot)
    for i in range(length_shot):
        # Define the codec and create VideoWriter object
        cap = []
        if i > 0:
            cap = cv2.VideoCapture(arr_uri_shot[i])
        else:
            cap = cap0
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for i in range(length):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if (ret != True):
                cap.release()
                break
            out.write(frame)
    out.release()
    cv2.destroyAllWindows()


# def fucntion to read video and then output image that represent for each shot
def dectUsingHSV(inputfile, outputfolder):
    """
    Function loads video then processing to produce shot, keyframe 
    with each video this function will created two folder:
    shot folder stores output shot, frame stores output keyframe
    :param inputfile: path to input video
    :param outputfolder: output folder
    :return: 
    """
    # load image
    cap = cv2.VideoCapture(inputfile)

    # create first output folder if not exist
    output_keyframe_path = outputfolder + "/frame/"
    output_keyframe_path2 = outputfolder + "/frame2/"
    output_shot_path = outputfolder + "/shot/"
    output_shot_path2 = outputfolder + "/shot2/"
    temp_folder = outputfolder + "/temp/"
    if not os.path.exists(output_keyframe_path): os.makedirs(output_keyframe_path)
    if not os.path.exists(output_keyframe_path2): os.makedirs(output_keyframe_path2)
    if not os.path.exists(output_shot_path): os.makedirs(output_shot_path)
    if not os.path.exists(output_shot_path2): os.makedirs(output_shot_path2)
    if not os.path.exists(temp_folder): os.makedirs(temp_folder)
    # get number frame/second, height-weight of video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    arr_hist = np.array([[[[]]]], dtype=np.float)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #img = cv2.imread('../../../data/video/output/anni011/frame88.jpg')
    #hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hist_new1 = cv2.calcHist \
    #    ([hsv1], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    #img2 = cv2.imread('../../../data/video/output/anni011/frame89.jpg')
    #hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    #hist_new2 = cv2.calcHist \
    #    ([hsv2], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    res = np.array([], dtype=np.float)
    new_frame = []
    old_frame = []
    # loop through all frame, calculating chi-square diffirence and storing to res array
    for i in range(length):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print (frame.shape)
        if (ret != True):
            break
        # Our operations on the frame come here

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist_new = cv2.calcHist\
            ([hsv], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
        # Display the resulting frame
        #cv2.imshow('frame', frame)
        #arr_hist = np.append(arr_hist, hist_new, axis=0)
        if i == 0:
            old_frame = hist_new
            new_frame = hist_new
        else:
            old_frame = new_frame
            new_frame = hist_new
        # diffrent between two frame using chi-square formular
        diffChiSquare = [cv2.compareHist(new_frame, old_frame, 1)]
        diff = [np.sum(np.absolute(old_frame - new_frame))]
        res = np.append(res, diffChiSquare, axis=0)

    # calculating mean and variance to creating the thresold
    var = np.sqrt(np.var(res))
    mean = np.mean(res)
    # panda -    best
    T = mean + 0.5 * var
    print("mean ", mean)
    print("var ", (var))
    print ("T ", T)
    plt.plot(res, color='r')
    plt.ylabel('distance')
    #plt.show()

    shotDect = [index for index in range(length) if (res[index] >= T)]
    index = 0
    index2 = 0
    lengthShot = len(shotDect)
    # set position frame to reread and get the keyframe in video
    cap.release()
    #cap.set(0, 0)
    cap = cv2.VideoCapture(inputfile)

    maxConstrast = 0
    imgchoice = []
    indexChoice = 0
    arrChoice = np.array([], dtype=np.int)
    """shot0path = output_shot_path + "shot0.avi"
    out = cv2.VideoWriter(shot0path, fourcc,e fps, (width, height))"""
    shot0path2 = output_shot_path2 + "shot0.avi"
    out2 = cv2.VideoWriter(shot0path2, fourcc, fps, (width, height))
    # loop through again video then get key frame and shot
    for i in range(length):
        # Capture frame-by-frameOCN/opencv/video_analysis/shot_detect_RSV_ROG.py:165
        ret, frame = cap.read()
        # calculate the constrast
        if (ret != True):
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # if this position frame is less than shotDect's position
        # then current position and before is in a same shot
        # add this to current shot
        # and calculating the contrast to choice be max contrast image to be keyframe

        """if (index < lengthShot) & (i < shotDect[index]):
            out.write(frame)
            constrast = calConstrastGray(gray)
            if i == 0:
                imgchoice = gray
            if (constrast > maxConstrast):
                maxConstrast = constrast
                imgchoice = gray
                indexChoice = i
        # if this position frame is shotDect's position
        # then store the keyframe, close this current shot to open and write new shot
        else:
            if i == 0:
                imgchoice = gray
            out.release()
            shotpath = output_shot_path + 'shot%d.avi' % index
            out = cv2.VideoWriter(shotpath, fourcc, fps,
                                  (width, height))
            arrChoice = np.append(arrChoice, indexChoice)
            cv2.imshow('frame', imgchoice)
            keypath = output_keyframe_path + "frame%d.jpg" % indexChoice
            cv2.imwrite(keypath, imgchoice)
            maxConstrast = calConstrastGray(gray)
            imgchoice = gray
            indexChoice = i
            index = index + 1
            if (index >= lengthShot):
                break
        """
        if (i==0):
            keypath2 = output_keyframe_path2 + "frame%d.jpg" % i
            cv2.imwrite(keypath2, gray)
        if( (index2 < lengthShot) & (i==int(shotDect[index2]) )):

            keypath2 = output_keyframe_path2 + "frame%d.jpg" % i
            cv2.imwrite(keypath2, gray)
            index2 = index2 + 1
            out2.release()
            shotpath = output_shot_path2 + 'shot%d.avi' % index2
            out2 = cv2.VideoWriter(shotpath, fourcc, fps,
                                  (width, height))
            out2.write(frame)
            if (index2 >= lengthShot):
                break
        else:
            out2.write(frame)

    # When everything done, release the capture and save metadata to file
    np.savetxt(outputfolder + "/shotdect.txt", shotDect)
    shotDect = np.insert(shotDect, 0 , [0])
    np.savetxt(outputfolder + "/choice.txt", shotDect)

    np.savetxt(outputfolder + "/hsv.txt", res)
    cap.release()
    out2.release()
    cv2.destroyAllWindows()


# def function to read ouput from first step using RSV,
# then continue filtering using ROG

def dectUsingROG(inputfolder):
    winSize = (64, 64)
    blockSize = (16, 16)
    blockStride = (8, 8)
    cellSize = (8, 8)
    nbins = 9
    derivAperture = 1
    winSigma = 4.
    histogramNormType = 0
    L2HysThreshold = 2.0000000000000001e-01
    gammaCorrection = 0
    nlevels = 64
    # read array shot in numpy array
    choiceFile = inputfolder + "/choice.txt"
    arrShot = np.loadtxt(choiceFile, dtype=np.float, delimiter="\n")
    lengthShot = arrShot.shape[0]
    img_before = []
    hist_before = []
    index_before = 0
    hog = cv2.HOGDescriptor()
    arrDiff = np.array([], np.int)

    # loop through each keyshot to calculate the diffirence using ROG histogram
    for i in range(lengthShot):
        if (i == 0):
            filename1 = inputfolder + "/frame2/frame" + str(int(arrShot[0])) + ".jpg"
            img_before = cv2.imread(filename1)
            hist_before = hog.compute(img_before)
            index_before = arrShot[0]

        else:
            filename2 = inputfolder + "/frame2/frame" + str(int(arrShot[i])) + ".jpg"

            img_current = cv2.imread(filename2)
            hist_current = hog.compute(img_current)
            index_current = arrShot[i]
            diff = hist_current - hist_before
            diff = np.sum(np.abs(diff))
            diff = diff / (10 ** 6)
            arrDiff = np.append(arrDiff, diff)

            img_before = img_current
            hist_before = hist_current
            index_before = index_current
    np.savetxt(inputfolder + "/rog.txt", arrDiff)
    # calculating the mean and variance to create thresold
    mean = np.mean(arrDiff)
    var = np.sqrt(np.var(arrDiff))
    T = mean
    print("mean ", mean)
    print("var ", var)
    # this variable to store list keyframe need to be concate because
    # these differences is less than the thresold
    arr_concat = []

    # folder to store results
    shot_folder = inputfolder + "/shot2"
    concat_shot_folder = inputfolder + "/rog/shot"
    rog_folder = inputfolder + "/rog"
    if not os.path.exists(rog_folder): os.makedirs(rog_folder)
    if not os.path.exists(concat_shot_folder): os.makedirs(concat_shot_folder)
    concat = 0
    # now loop through again, find and store best keyframe and shot
    for i in range(lengthShot):
        uri = shot_folder + "/shot%d.avi" % i
        if (i == 0):
            filename1 = inputfolder + "/frame2/frame" + str(int(arrShot[0])) + ".jpg"
            #
            # print filename1
            img_before = cv2.imread(filename1)
            index_before = arrShot[0]
            arr_concat.append(uri)
        else:
            filename2 = inputfolder + "/frame2/frame" + str(int(arrShot[i])) + ".jpg"
            img_current = cv2.imread(filename2)
            index_current = arrShot[i]
            diff = arrDiff[i - 1]

            if diff < T:
                arr_concat.append(uri)
                constrast_before = calConstrastColor(img_before)
                constrast_current = calConstrastColor(img_current)

                if (constrast_before < constrast_current):
                    img_before = img_current
                    index_before = index_current
                if (i == (lengthShot - 1)): break
            else:
                # save both image
                keypath1 = inputfolder + "/rog/frame%d.jpg" % index_before
                keypath2 = inputfolder + "/rog/frame%d.jpg" % index_current
                cv2.imwrite \
                    (keypath1, img_before)
                # concat and save shot
                concat_shot(arr_concat, concat_shot_folder + "/shot%d.avi" % concat)

                arr_concat = [uri]
                concat = concat + 1
                img_before = img_current
                index_before = index_current
                if( i == (lengthShot-1) ):
                    cv2.imwrite \
                        (keypath2, img_current)
                    concat_shot(arr_concat, concat_shot_folder + "/shot%d.avi" % concat)

def detect_using_HSV_ROG(video_uri, output_folder):
    # TODO: analysis
    dectUsingHSV(video_uri, output_folder)
    dectUsingROG(output_folder)


if __name__ == '__main__':
    detect_using_HSV_ROG("../../../data/video/anni001.mpg",
                         "../../../data/video/output/anni001")
    #load_and_show_histogram("../../../data/video/output/daddy_and_baby", "hsv")
