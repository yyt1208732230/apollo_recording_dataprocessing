

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from util import *
from envload import *

def run_gps_visualization():
    # fixgpschassis = pd.read_csv('./p01/fixgpschassis--20230414120746.record.csv',
    #                             usecols=[ 1,2,3])
    PName = PNAME
    fixgpschassis = pd.read_csv(CANBUS_FOLDER_PATH + 'fixgpschassis--' + APOLLO_RECORD_FILE_INDEX + '.csv',
                                usecols=[ 1,2,3])


    data_fixgpschassis = fixgpschassis.iloc[:,0:3]
    data_fixgpschassis = np.array(data_fixgpschassis)
    print(data_fixgpschassis.shape)
    time = data_fixgpschassis[:,0]
    longitude = data_fixgpschassis[:,2]
    latitude = data_fixgpschassis[:,1]
    print(time.shape)
    print(time[0])
    print(longitude.shape)
    print(longitude[0])
    print(latitude.shape)
    print(latitude[0])

    # part_latitude = latitude[130000:-1]
    # part_longitude = longitude[130000:-1]

    #  A1   135280,       ,137000 ,  ,
    x_a1 = np.array([113.6262733,  113.6266467])
    y_a1 = np.array([38.00832967,  38.00860633])

    #  A2 139800  140425, 141200      ,  ,
    x_a2 = np.array([113.629055, 113.6294783, 113.6303367])
    y_a2 = np.array([38.00867467, 38.008718, 38.00879133])

    #  D1     ,147840    149600   154450
    x_d1 = np.array([ 113.6335634,  113.6338401, 113.6335834])
    y_d1 = np.array([ 38.008913,  38.00892633, 38.00897467])


    #  A3 156800, 157700      ,  ,
    x_a3 = np.array([113.6294917, 113.6290017])
    y_a3 = np.array([38.00882133, 38.00917467])

    #  A4 160500, 161300      ,  ,
    x_a4 = np.array([113.6292733, 113.6297433])
    y_a4 = np.array([38.011498, 38.01184633])

    #  L1   165100,   166600    , ,  ,
    x_l1 = np.array([113.6341434, 113.6345384])
    y_l1 = np.array([38.01211467, 38.012473])

    #  L2   168300,   169700    , ,  ,
    x_l2 = np.array([113.6344051, 113.6339534])
    y_l2 = np.array([38.013393, 38.013638])

    #  R1   173400,   174800    , ,  ,
    x_r1 = np.array([113.6295317, 113.62911])
    y_r1 = np.array([38.013433, 38.013848])

    #  R2   176200,   177200    , ,  ,
    x_r2 = np.array([113.6290783, 113.62939])
    y_r2 = np.array([38.01488133, 38.015263])

    #  R3 179500, 180800      ,  ,
    x_r3 = np.array([113.6336234, 113.6341834])
    y_r3 = np.array([38.01541967, 38.01510133])

    #  R4 182900, 186500      ,  ,
    x_r4 = np.array([113.6343017,113.6335251])
    y_r4 = np.array([38.01400133, 38.01363133])

    #  L3 190000, 191400      ,  ,
    x_l3 = np.array([113.6296583, 113.6291083])
    y_l3 = np.array([38.01345133, 38.01296467])

    # img = plt.imread("rain.jpg")
    # plt.imshow(img, extent=[-5, 80, -5, 30])
    plt.scatter(longitude, latitude, alpha=0.5, marker='s', label='Tracking Route' )
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.scatter(x_a1 , y_a1, alpha=0.85, label='A1 (Turn Left)' )
    plt.scatter(x_a2 , y_a2, alpha=0.85, label='A2 (Lane Change)'  )
    plt.scatter(x_d1 , y_d1, alpha=0.85, label='D1 (Turn Around)'  )
    plt.scatter(x_a3 , y_a3, alpha=0.85, label='A3 (Turn Right)'  )
    plt.scatter(x_a4 , y_a4, alpha=0.85, label='A4 (Turn Right)'  )
    plt.scatter(x_l1 , y_l1, alpha=0.85, label='L1 (Turn Left)'  )
    plt.scatter(x_l2 , y_l2, alpha=0.85, label='L2 (Turn Left)'  )
    plt.scatter(x_r1 , y_r1, alpha=0.85, label='R1 (Turn Right)' )
    plt.scatter(x_r2 , y_r2, alpha=0.85, label='R2 (Turn Right)'  )
    plt.scatter(x_r3 , y_r3, alpha=0.85, label='R3 (Turn Right)'  )
    plt.scatter(x_r4 , y_r4, alpha=0.85, label='R4 (Turn Right)'  )
    plt.scatter(x_l3 , y_l3, alpha=0.85, label='L3 (Turn Left)'  )
    plt.legend()
    plt.title("GPS Tracking Route (" + PName + ")")
    plt.show()
    plt.savefig("P04-GPS Tracking Route.png")
    pass


run_gps_visualization()



