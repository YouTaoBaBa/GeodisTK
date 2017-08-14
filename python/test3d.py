import geodesic_distance
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
import nibabel

def load_nifty_volume_as_array(filename):
    # input shape [W, H, D]
    # output shape [D, H, W]
    img = nibabel.load(filename)
    data = img.get_data()
    data = np.transpose(data, [2,1,0])
    return data

def save_array_as_nifty_volume(data, filename):
    # numpy data shape [D, H, W]
    # nifty image shape [W, H, W]
    data = np.transpose(data, [2, 1, 0])
    img = nibabel.Nifti1Image(data, np.eye(4))
    nibabel.save(img, filename)

def test_geodesic_distance3d():
    
    I = load_nifty_volume_as_array("../data/img3d.nii")
    I = np.asarray(I, np.float32)
    I = I[0:40, 50:150, 50:150]
    S = np.zeros_like(I, np.uint8)
    S[25][50][50] = 1
    t0 = time.time()
#    D1 = geodesic_distance.geodesic3d_fast_marching(I,S)
    t1 = time.time()
    D2 = geodesic_distance.geodesic3d_raster_scan(I,S, 0.5)
    dt1 = t1 - t0
    dt2 = time.time() - t1
    print "runtime(s) fast marching {0:}".format(dt1)
    print "runtime(s) raster scan   {0:}".format(dt2)

    max_iten = D2.max()
    D2 = D2*255/max_iten
    D2 = np.asarray(D2, np.uint8)
    save_array_as_nifty_volume(D2, "../data/image3d_dis2.nii")
    
    
    I = I*255/I.max()
    I = np.asarray(I, np.uint8)
    save_array_as_nifty_volume(I, "../data/image3d_sub.nii")

if __name__ == '__main__':
    test_geodesic_distance3d()