import os
import numpy as np

from torch.utils.data import DataLoader
from utils.dataloader import FRCNNDataset, frcnn_dataset_collate
#---------------------------------------------#
#    将生成的伪标签文件和原来的注释文件结合      
#---------------------------------------------#
#伪标签文件：pseudo.txt
#原注释文件：human_train.txt

def fetch(lines):
    annotation=[]
    num=len(lines)
    for i in range(num):
        line = lines[i]
        line = line.split()
        img = {}
        # print(line)
        path = line[0]
        # print('path:', path)
        img['path']=path
        boxes = []
        if len(line) >= 2:
            # print('have pseudo box!')
            for j in range(1,len(line)):
                boxes.append(line[j])
            # print('boxes:',boxes)
        img['box']=boxes
        annotation.append(img)
    # print(orig_annotation)
    return annotation



if __name__ == "__main__":

    input_shape     = [900, 1600]
    #修改path
    orig_path = 'pseudo.txt'
    pseudo_path = 'pseudo.txt'

    with open(orig_path, encoding='utf-8') as f:
        orig_lines = f.readlines()
    with open(pseudo_path, encoding='utf-8') as f:
        pseudo_lines = f.readlines()

    num_orig = len(orig_lines)
    num_pseudo = len(pseudo_lines)

    orig_annotation = fetch(orig_lines)
    pseudo_annotation = fetch(pseudo_lines)
    # print(pseudo_annotation)
    merge_annotation = orig_annotation
    for orig in merge_annotation:
        img_path = orig['path']
        for pseudo in pseudo_annotation:
            if pseudo['path'] == img_path:
                 for box in pseudo['box']:
                    orig['box'].append(box)
    print(len(merge_annotation))

    # 将merge_annotation写入txt
    filename = 'merge'
    list_file = open('%s.txt'%(filename), 'w', encoding='utf-8')
    for img in merge_annotation:
        list_file.write(img['path'])
        #bbox & category
        for box in img['box']:
            list_file.write(" " + box )
        list_file.write('\n')
    list_file.close()
    print('Generate %s.txt'%(filename))