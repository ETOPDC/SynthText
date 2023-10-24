import json

# 读取第一个 JSON 文件
with open("file1.json", "r", encoding='utf-8') as f1:
    data1 = json.load(f1)

# 读取第二个 JSON 文件
with open("file2.json", "r", encoding='utf-8') as f2:
    data2 = json.load(f2)

# 合并数据结构
merged_data = {
    "metainfo": data1["metainfo"],
    "data_list": data1["data_list"] + data2["data_list"]
}

# 写入合并后的数据结构到新的 JSON 文件
with open("merged_file.json", "w", encoding='utf-8') as f:
    json.dump(merged_data, f, indent=4)
