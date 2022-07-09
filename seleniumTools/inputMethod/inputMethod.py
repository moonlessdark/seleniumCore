# coding=utf-8

import os

command0 = 'adb shell ime list -s'
command1 = 'adb shell settings get secure default_input_method'
command2 = 'adb shell ime set com.sohu.inputmethod.sogou.xiaomi/.SogouIME'
command3 = 'adb shell ime set io.appium.android.ime/.UnicodeIME'
command4 = 'adb shell ime set com.baidu.input_huawei/.ImeService'
command5 = 'adb shell ime set com.meizu.flyme.input/com.meizu.input.MzInputService'

"""
---------------------------------------
    列出系统现在所安装的所有输入法
    os.system(command0)
    
    打印系统当前默认的输入法
    os.system(command1)
    
    切换latin输入法为当前输入法
    os.system(command2)
    
    切换appium输入法为当前输入法
    os.system(command3)
    
    切换appium输入法为当前输入法
    os.system(command4)
--------------------------------------
注意，该方法并非完美解决输入法的方法，当同时连接多台手机的时候，可能会出现其他问题
-----------------------------------------------------------------------------
"""


class InputMethod:

    # 切换meizu输入法为当前输入法
    @staticmethod
    def enable_meizu_ime():
        os.system(command5)

    # 切换appium输入法为当前输入法
    @staticmethod
    def enable_appium_unicode_ime():
        os.system(command3)

    # 切换位百度输入法华为专版
    @staticmethod
    def enable_baidu_huawei_ime():
        os.system(command4)
