#!C:\myDevTools\Python27\python
# -*- coding: utf-8 -*-
#
# �����ļ��ӽ���
# ʹ�÷�����python decrypt_aes_file.py  [e|d] file_name.jpg  dest_dir
#

import os
import sys
from Crypto.Cipher import AES

_key = "lhdlhd6666666666".encode("gbk")

_dir = "E:/share/aes_data/"

try:
    if len(sys.argv) < 4:
        #_dowhat = raw_input(unicode('>>> �������� e �������� d:\n>>> ').encode('gbk'))
        #_name = raw_input(unicode('>>> �������ļ���:\n>>> ').encode('gbk'))
        #_dir = raw_input(unicode('>>> ������洢λ��:\n>>> ').encode('gbk'))
        _dowhat = raw_input(unicode('>>> ecrypt: e decrypt: d:\n>>> ').encode('gbk'))
        _name = raw_input(unicode('>>> input filename:\n>>> ').encode('gbk'))
        _diri = raw_input(unicode('>>> input save path:\n>>> ').encode('gbk'))
    else:
        _dowhat = str(sys.argv[1])
        _name = str(sys.argv[2])
        _diri = str(sys.argv[3])

    if _diri == "":
        _diri = _dir
                
    #�ļ��ı���Ŀ¼
    os.chdir(_diri)

    with open(_name, "rb") as f:
        content = f.read()
        f.close()

    #�����ܵ����ݣ�������16�ı�����������ǣ�����Ҫ����֮.�㷨���£�
    #pkcs#5 / PKCS#7�Ķ��壺�������һ���ֲ������鳤��(128λaes����֮ecbģʽ��16)�����ݣ�
    #����Ҫ�����ֽڵĳ���Ϊʣ�೤��n����������ÿ���ֽڵ����ݼ�Ϊʣ�೤��n��ʮ�����ơ�
    #�������ٶ����ݣ�FF FF FF FF FF FF FF FF FF(���ݵĳ���Ϊ 9)���鳤��Ϊ16������£�
    #����Ҫ���16-9=7λ���ݣ���������ֽ�Ҳ��07����PKCS7����Ľ����
    #FF FF FF FF FF FF FF FF FF 07 07 07 07 07 07 07

    if _dowhat == 'e': #����
        padadd = 16 - len(content) % 16
        content = content + (chr(padadd) * padadd)
        _name = _name + ".lhde"
    else:
        _name = _name[0:len(_name)-5] #���ܺ�ȥ���ļ����е� '.lhde' ��չ��׺��.

    with open(_name, "wb") as fw:
        #cryptor = AES.new(_key, AES.MODE_CBC, _key) #AES.MODE_CBC ��Ҫ iv�� ECB����Ҫiv
        cryptor = AES.new(_key, AES.MODE_ECB) #AES.MODE_CBC ��Ҫ iv�� ECB����Ҫiv
        
        if _dowhat == 'e': #����
            fw.write(cryptor.encrypt(content))
        else:
            #���ܺ��������Ҫȥ��֮ǰ������ӵĲ����ַ�
            od = cryptor.decrypt(content)
            od_length = len(od)
            paddingChar = od[od_length - 1:]
            paddingLength = ord(paddingChar)
            #�����ܲ�ȥ��padding�ַ��������д���ļ�.
            fw.write(od[:-paddingLength])
        fw.flush()
        fw.close()

    print _name + "\n--end--"

except Exception as e:
    print e

