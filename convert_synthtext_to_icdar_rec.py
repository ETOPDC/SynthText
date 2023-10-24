"""
    生成只带文字的小区域
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
    im_n = 0
    im_name_label = []
    os.makedirs(f'scene_text_recognition/', exist_ok=True)
    os.makedirs(f'scene_text_recognition/images/', exist_ok=True)

    for item in tqdm(range(len(dsets))):
        k = dsets[item]
        rgb = db['data'][k][...]
        wordBB = db['data'][k].attrs['wordBB']
        txt = db['data'][k].attrs['txt']
        txt = [prepare_text(i).split(' ') for i in txt]
        txt = list(itertools.chain(*txt))

        for image_item, im_text in zip(range(wordBB.shape[-1]), txt):

            bb = wordBB[:, :, image_item]
            bb = np.c_[bb, bb[:, 0]]

            img_cutted = rgb[int(min(bb[1])):int(max(bb[1])), int(min(bb[0])):int(max(bb[0]))]

            im_name = f'{im_n}.png'
            try:
                cv2.imwrite(f'scene_text_recognition/images/{im_name}', img_cutted,
                            [cv2.IMWRITE_PNG_COMPRESSION, 0])
                im_name_label.append([im_name, im_text])
            except:
                print(OSError)
                im_n += 1
                continue
            im_n += 1
    df = pd.DataFrame(im_name_label)
    with open("scene_text_recognition/labels.txt", "w", encoding='UTF-8') as fo:
        for index in tqdm(range(df.shape[0])):
            file_name = df.iloc[index][0]
            text = df.iloc[index][1]
            fo.write(file_name + '\t' + text + '\n')