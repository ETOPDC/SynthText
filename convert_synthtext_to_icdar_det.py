"""
    将得到的h5文件转换为ICDAR2015格式
"""
import os
import h5py
from natsort import natsorted
import itertools
import cv2
import numpy as np
import pandas as pd
import regex as re
from tqdm import tqdm

def prepare_text(text):
    '''general text preparation'''
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

if __name__=="__main__":
    db = h5py.File('results/SynthText_8000.h5', 'r')
    dsets = natsorted(db['data'].keys())
    print("total number of images : ", len(dsets))
    im_n = 30059
    os.makedirs(f'scene_text_detection/', exist_ok=True)
    os.makedirs(f'scene_text_detection/imgs/', exist_ok=True)
    os.makedirs(f'scene_text_detection/annotations/', exist_ok=True)

    for item in tqdm(range(len(dsets))):
        im_name_label = []
        k = dsets[item]
        rgb = db['data'][k][...]
        wordBB = db['data'][k].attrs['wordBB']
        txt = db['data'][k].attrs['txt']
        txt = [prepare_text(i).split(' ') for i in txt]
        txt = list(itertools.chain(*txt))

        im_name = f'img_{im_n}.jpg'
        try:
            cv2.imwrite(f'scene_text_detection/imgs/{im_name}', cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB),
                        [cv2.IMWRITE_JPEG_QUALITY, 100])
            for image_item, im_text in zip(range(wordBB.shape[-1]), txt):
                bb = wordBB[:, :, image_item]
                bb = np.c_[bb, bb[:, 0]]
                im_name_label.append([int(bb[0,0]),int(bb[1,0]),int(bb[0,1]),int(bb[1,1]),int(bb[0,2]),int(bb[1,2]),int(bb[0,3]),int(bb[1,3]),im_text])
        except:
            print(OSError)
            im_n += 1
            continue
        with open(f"scene_text_detection/annotations/gt_img_{im_n}.txt", "w", encoding='UTF-8') as fo:
            for j in im_name_label:
                fo.writelines("".join(str(j)).replace("[","").replace("]","").replace("'","").replace(" ","")+"\n")
        im_n += 1

    print("im_n : ", im_n)
