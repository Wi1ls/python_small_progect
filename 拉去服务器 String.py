#服务器 String 多语言下，自动下载并且 overwrite 对应的多语言 xml
import requests
import json
import os
import zipfile

seg = os.sep
#公司 host 与自己的账号密码，匿掉了
host = ""
loginData = {'username': '', "password": ''}
#工程项目所在的文件夹
localProjectDir = "/Users/wi1ls/app/lollypop"
localStringDir = 'lollypop-client-android/common/base/femometer_strings/src/main/res'
#目标 string 所在的文件夹
localTargetDir = localProjectDir + os.sep + localStringDir
#多语言，中文，英文，德语，土耳其对应的文件夹和 xml 文件名字
folders = ('values', 'values-de', 'values-tr', 'values-zh-rCN')
files = {'values': 'English.xml', 'values-de': 'German.xml', 'values-tr': 'Turkish.xml',
         'values-zh-rCN': 'Chinese.xml'}
#下载的服务器 string 文件压缩包，temp，解压后删除
tempFile = localTargetDir + seg + "Android.zip"
appFlag = str(4)


# 登录,获取 cookies，记录登录状态后进行后续网络操作
def getLoginCookies():
    session = requests.session()

    try:
        session.post(host + "/auth/login/", data=loginData)
        print('---开始登陆---')
        print('---cookies=', session.cookies, "---")
        return session
    except:
        print("无网络或者请求失败，请检查参数")
        exit()

# 获取网络上最新的版本号
def getServerLastVersion(session):
    # 棒米体温计的 appFlag

    try:
        queryVersionResponse = requests.get(host + "/text/version?app=" + appFlag, cookies=session.cookies)
    except:
        print("发生错误，请检查网络或者服务器")
        exit()

    versionList = json.loads(queryVersionResponse.content)

    # 服务器上的最新版本
    lastVersion = versionList['versions'][0]['name']
    return lastVersion


# 获取本地最新的版本号
def getLocalLastVersion():
    englishFile = open(localTargetDir + seg + folders[0] + seg + files[folders[0]], 'r', encoding='utf-8')
    for line in englishFile.readlines():
        if line.__contains__('Version'):
            parts = line.split(" ")
            # <!-- Version 0.0.485 -->
            return parts[2]
            break;

#开始下载服务器上的文件
def downloadFromServer(app, version, session):
    print("---开始下载文件---")
    downUrl = host + "/text/export_Andriod?app=" + app + "&version=" + version
    downR = requests.get(downUrl, cookies=session.cookies)
    with open(tempFile, "wb") as code:
        code.write(downR.content)
    print('---下载文件成功---')
    return zipfile.ZipFile(tempFile)


loginCookies = getLoginCookies()
serverVersion = getServerLastVersion(loginCookies)
print("服务器最新版本号:", serverVersion)
localVersion = getLocalLastVersion()
print("本地最新版本号", localVersion)
if (serverVersion > localVersion):
    print("服务器版本比较高")
    #解压到对应的目录
    stringZipFile = downloadFromServer(appFlag, serverVersion, loginCookies)
    for fileInZip in stringZipFile.namelist():
        for folder, fileName in files.items():
            if (fileInZip == fileName):
                stringZipFile.extract(fileInZip, localTargetDir + seg + folder)
    stringZipFile.close()
    os.remove(tempFile)
else:
    print("本地版本与服务器一致")
