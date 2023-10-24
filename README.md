Modify from :

    https://github.com/ankush-me/SynthText/tree/python3

    https://github.com/JarveeLee/SynthText_Chinese_version

    https://github.com/LaJoKoch/SynthTextGerman


用于合成中文，藏文，维吾尔文，德宏傣文，蒙文

## install

windows10

```
conda create --name synthtextpy3 python=3.6
conda activate synthtextpy3
pip install -r requirements.txt
```



## run
1. 将字体文件放入data/fonts文件夹下
2. 修改`fontlist.txt`
3. 运行
`
python .\invert_font_size.py
`
生成`data/models/font_px2pt.cp`文件

4. 修改newsgroup.txt文件
5. 运行`python update_freq.py` `生成char_freq.cp`文件

6. `
python gen.py`
or
`python gen_more.py
`

想生成曲线文本，请参考：
https://github.com/PkuDavidGuan/CurvedSynthText/tree/master
对`synthgen.py`文件进行修改

you can use `add_more_data.py` to gen 8000 background picture, you should put 