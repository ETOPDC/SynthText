import json
import os
from PIL import Image

def polygon_to_bbox(polygon):
    min_x = min(polygon[::2])
    min_y = min(polygon[1::2])
    max_x = max(polygon[::2])
    max_y = max(polygon[1::2])
    bbox = [min_x, min_y, max_x, max_y]
    return bbox

# 构建数据结构
data = {
    "metainfo": {
        "dataset_type": "TextDetDataset",
        "task_name": "textdet",
        "category": [{"id": 0, "name": "text"}]
    },
    "data_list": []
}
gt_dir = "scene_text_detection/annotations"
img_dir = "scene_text_detection/imgs"
json_path = "scene_text_detection/output.json"
items = os.listdir(img_dir)
for item in items:
    new_data = {}
    new_data["img_path"] = "imgs/"+item

    img_path = os.path.join(img_dir, item)
    image = Image.open(img_path)
    # 获取图像的宽度和高度
    new_data["height"] = image.height
    new_data["width"] = image.width

    #获取instances
    new_data["instances"] = []
    gt_path = os.path.join(gt_dir,"gt_"+os.path.splitext(item)[0]+".txt")
    if(os.path.isfile(gt_path)):
        with open(gt_path,"r", encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 去除行尾的换行符

                # 创建一个instance
                new_instance = {}

                #获取polygon
                numbers_str = line.split(',')[0:-1]
                text_str = line.split(',')[-1]
                numbers = list(map(int, numbers_str))
                new_instance["polygon"] = numbers

                new_instance["bbox"] = polygon_to_bbox(numbers)
                new_instance["bbox_label"] = 0
                new_instance["text"] = text_str
                if(text_str=="###"):
                    new_instance["ignore"] = True
                else:
                    new_instance["ignore"] = False
                new_data["instances"].append(new_instance)
        data["data_list"].append(new_data)
    else:
        print(gt_path + " is not exist!!!")

# 将数据结构转换为JSON字符串
json_data = json.dumps(data, ensure_ascii=False,indent=4)

# 保存JSON字符串到文件
with open(json_path, "w", encoding='utf-8') as f:
    f.write(json_data)

