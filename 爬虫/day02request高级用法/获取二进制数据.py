#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re

# response=requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1509868306530&di=712e4ef3ab258b36e9f4b48e85a81c9d&imgtype=0&src=http%3A%2F%2Fc.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F11385343fbf2b211e1fb58a1c08065380dd78e0c.jpg')
#
# with open('a.jpg','wb') as f:
#     f.write(response.content)

# response = requests.get('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1516187549857&di=dd9e11ee70638cccd854dd504d9565d4&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2Fdbb44aed2e738bd41f16dd0daa8b87d6277ff9d3.jpg')
#
# with open('b.jpg','wb') as f:
#     f.write(response.content)

response = requests.get('https://gss3.baidu.com/6LZ0ej3k1Qd3ote6lo7D0j9wehsv/tieba-smallvideo-transcode/1767502_56ec685f9c7ec542eeaf6eac93a65dc7_6fe25cd1347c_3.mp4',stream=True)

with open('b.mp4','wb') as f:
    for line in response.iter_content():
        f.write(line)