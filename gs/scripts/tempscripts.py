# -*- coding:utf-8 -*-
from gs.common.cstore import get_token
from qiniu import put_file

if __name__ == '__main__':
    token = get_token()
    ret, info = put_file(token, key='avatar.jpg',
                         file_path='C:\Users\99100\Documents\Tencent Files\991007889\FileRecv\MobileFile\\face.jpg')
    print ret, info
