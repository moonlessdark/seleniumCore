# encoding:utf-8
import subprocess

from seleniumTools.logger.log import Logger
import os
import requests
import winreg
import zipfile

url = 'https://npm.taobao.org/mirrors/chromedriver/'
log = Logger(logger="检查驱动")


def get_chrome_version() -> str:
    """
    通过注册表检查windows电脑中安装的谷歌浏览器的版本
    :return:
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    if version is None or version == "":
        version = 0  # 表示电脑没有安装浏览器
    return version


def get_server_chrome_versions() -> list:
    """
    获取服务端的所有版本号
    :return:
    """
    versionList = []
    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    rep = requests.get(url).json()
    rep = rep[::-1]
    for item in rep:
        versionList.append(item["name"])
    return versionList


def download_driver(download_url: str):
    """
    从网站上下载驱动文件
    :param download_url: 下载url
    :return:
    """
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        log.info('下载成功')


def get_version(file_path: str):
    """
    查询传入的驱动文件Chromedriver的版本
    :param file_path: 驱动目录，不包含驱动文件名
    :return:
    """
    b = os.popen("set path=" + file_path + "&&chromedriver")
    c = b.readline()
    subprocess.Popen("taskkill /f /im chromedriver.exe", stdout=subprocess.PIPE, shell=False).stdout.readlines()
    return c.split(" ")[2]


def unzip_driver(path: str):
    """
    解压Chromedriver压缩包到指定目录
    :param path: 解压路径
    :return:
    """
    f = zipfile.ZipFile("chromedriver.zip", 'r')
    for file in f.namelist():
        f.extract(file, path)


def check_path(file_path: str):
    """
    检查驱动路径
    :param file_path: 驱动文件路径
    :return: chrome_driver_path
    """
    file_path = file_path.replace("\\", "/")
    if "chromedriver.exe" in file_path:
        right_folder_index = file_path.rfind("/")
        file_path_folder = file_path[:right_folder_index+1]
        return file_path_folder
    else:
        log.info("请保持驱动的名称为：chromedriver.exe")
        return file_path


def check_update_chromedriver(file_path: str):
    """
    检查windows系统的chromeDriver驱动版本是否一致
    :param file_path: 本地的chromedriver路径
    :return:
    """

    file_path = check_path(file_path)
    chromeVersion = get_chrome_version()
    chrome_main_version = int(chromeVersion.split(".")[0])  # chrome主版本号
    driver_main_version = ''
    if os.path.exists(os.path.join(file_path, "chromedriver.exe")):
        driverVersion = get_version(file_path)
        driver_main_version = int(driverVersion.split(".")[0])  # chromedriver主版本号
    download_url = ""
    if driver_main_version != chrome_main_version:
        log.info("chromedriver版本与chrome浏览器不兼容，更新中>>>")
        versionList = get_server_chrome_versions()
        if chromeVersion in versionList:
            download_url = f"{url}{chromeVersion}/chromedriver_win32.zip"
        else:
            for version in versionList:
                if version.startswith(str(chrome_main_version)):
                    download_url = f"{url}{version}/chromedriver_win32.zip"
                    break
            if download_url == "":
                log.info("暂无法找到与chrome兼容的chromedriver版本，请在http://npm.taobao.org/mirrors/chromedriver/ 核实。")

        download_driver(download_url=download_url)
        path = file_path
        unzip_driver(path)
        os.remove("chromedriver.zip")
        log.info('更新后的Chromedriver版本为：%s' % get_version(file_path))
    else:
        log.info("chromedriver版本与chrome浏览器相兼容，无需更新chromedriver版本！")
    return os.path.join(file_path, "chromedriver.exe")


if __name__ == '__main__':
    check_update_chromedriver(file_path="D:/Program Files/drives/chromedriver_win32/")
