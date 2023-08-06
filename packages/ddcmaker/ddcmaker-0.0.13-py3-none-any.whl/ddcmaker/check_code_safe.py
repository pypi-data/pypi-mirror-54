"""
代码安全性检查，为了抵抗沙碧星人的入侵，在代码正式运行之前，需要做一个代码的全身检查，确保没有危险性代码的输入和可能危害系统安全性问题的代码
"""
import os
import time
import ddcmaker
import re


class read_code(object):

    def __find_method_name__(self, code):
        self.code = code
        find_name = "os"
        resultlist=re.search(self.code, find_name)
        print(resultlist)


# coding=utf-8
def find_all(source,dest):
    length1,length2 = len(source),len(dest)
    dest_list = []
    temp_list = []
    if length1 < length2:
        return -1
    i = 0
    while i <= length1-length2:
        if source[i] == dest[0]:
            dest_list.append(i)
        i += 1
    if dest_list == []:
        return -1
    for x in dest_list:
        print("Now x is:%d. Slice string is :%s"% (x,repr(source[x:x+length2])),end=" ")
        if source[x:x+length2] != dest:
            print(" dest != slice")
            temp_list.append(x)
        else:
            print(" dest == slice")
    for x in temp_list:
        dest_list.remove(x)
    return dest_list

# s1="He!wworld!www.baidu.cowws.cowwppww"
# s2=" ww"
# index_list = find_all(s1,s2)
# if index_list != -1:
#     print("Now dest_list is:{}".format(index_list))
# else:
#     print("Error finding!")


