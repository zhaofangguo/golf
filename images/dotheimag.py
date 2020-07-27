# -*- encoding: utf-8 -*-
"""
@File    :   dotheimag.py

@Contact :   2055466817@qq.com

@Modify Time :   2020/7/25 下午10:16

@Author :   赵方国
"""


from PIL import Image

IMAGE_SIZE_W = 320  # 每张小图片的宽
IMAGE_SIZE_H = 240  # 每张小图片的高

IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 2  # 图片间隔，也就是合并成一张图后，一共有几列

# 获取图片集地址下的所有图片名称
image_names = ['hole_afternoon.jpg', 'hole_afternoon2.jpg', 'hole_afternoontop.jpg', 'hole_afternoontop2.jpg']

# 简单的对于参数的设定和实际图片集的大小进行数量判断
print len(image_names)
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")

# 定义图像拼接函数
to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE_W, IMAGE_ROW * IMAGE_SIZE_H))  # 创建一个新图

# 循环遍历，把每张图片按顺序粘贴到对应位置上
for y in range(1, IMAGE_ROW + 1):
    for x in range(1, IMAGE_COLUMN + 1):
        from_image = Image.open(image_names[IMAGE_COLUMN * (y - 1) + x - 1])
        to_image.paste(from_image, ((x - 1) * IMAGE_SIZE_W, (y - 1) * IMAGE_SIZE_H))

to_image.save('finalafterhole.jpg')  # 保存新图

print 'work done'
