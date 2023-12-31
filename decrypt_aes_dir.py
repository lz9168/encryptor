#!C:\myDevTools\Python27\python
# -*- coding: utf-8 -*-
# 
# 整目录加解密
# 使用方法：python decrypt_aes_dir.py  [e|d]
#

import os
import sys
from Crypto.Cipher import AES

_key = "lhdlhd6666666666".encode("gbk")

_dir = "E:/share/aes_data/"

def do(dowhat):
    try:
        if dowhat == 'e':
            _rdir = _dir + "src/"
            _wdir = _dir + "enc/"
        else:
            _rdir = _dir + "enc/"
            _wdir = _dir + "src/"
            
        list = os.listdir(_rdir)
        for _name in list:
            with open(_rdir + _name, "rb") as f:
                content = f.read()
                f.close()

            #待加密的内容，必须是16的倍数，如果不是，则需要补齐之.算法如下：
            #pkcs#5 / PKCS#7的定义：对于最后一部分不足区块长度(128位aes加密之ecb模式是16)的数据，
            #若需要填充的字节的长度为剩余长度n，则需填充的每个字节的内容即为剩余长度n的十六进制。
            #举例，假定数据：FF FF FF FF FF FF FF FF FF(数据的长度为 9)，块长度为16的情况下，
            #则需要填充16-9=7位数据，因此填充的字节也是07，用PKCS7填充后的结果：
            #FF FF FF FF FF FF FF FF FF 07 07 07 07 07 07 07

            if dowhat == 'e': #加密
                padadd = 16 - len(content) % 16
                content = content + (chr(padadd) * padadd)
                _name = _name + ".lhde"
            else:
                _name = _name[0:len(_name)-5] #解密后，去掉文件名中的 '.lhde' 扩展后缀名.

            with open(_wdir + _name, "wb") as fw:
                #cryptor = AES.new(_key, AES.MODE_CBC, _key) #AES.MODE_CBC 需要 iv， ECB不需要iv
                cryptor = AES.new(_key, AES.MODE_ECB) #AES.MODE_CBC 需要 iv， ECB不需要iv
                
                if dowhat == 'e': #加密
                    fw.write(cryptor.encrypt(content))
                else:
                    #解密后的内容需要去掉之前可能添加的补齐字符
                    od = cryptor.decrypt(content)
                    od_length = len(od)
                    paddingChar = od[od_length - 1:]
                    paddingLength = ord(paddingChar)
                    #将解密并去掉padding字符后的数据写入文件.
                    fw.write(od[:-paddingLength])
                fw.flush()
                fw.close()

            print _name + "\n--end--"
    except Exception as e:
        print e
   

if __name__ == "__main__":
    try:
        print "\nworking at 'E:\share\aes_data'\n# python decrypt_aes_dir.py  [e|d]\n"
        
        if len(sys.argv) < 2:
            #_dowhat = raw_input(unicode('>>> 加密输入 e 解密输入 d:\n>>> ').encode('gbk'))
            #_name = raw_input(unicode('>>> 请输入文件名:\n>>> ').encode('gbk'))
            #_dir = raw_input(unicode('>>> 请输入存储位置:\n>>> ').encode('gbk'))
            _dowhat = raw_input(unicode('>>> ecrypt: e decrypt: d:\n>>> ').encode('gbk'))
        else:
            _dowhat = str(sys.argv[1])

        #文件的保存目录
        os.chdir(_dir)
        
        #执行加解密
        do(_dowhat)
    except Exception as e:
        print e
   
   