import subprocess
import sys
import re


# enum4linuxの出力を確認するための関数
# 後で削除予定
def testExecute(option, ip):
    try:
        args = ["enum4linux", option, ip]
        res = subprocess.check_output(args)
    except:
        return -1

    return res


def enumExecute(option, ip):
    """enum4linuxを実行するための関数。
    正しく実行されれば結果が返り、
    問題が発生した場合は-1を返す。

    Args:
        option (String): enum4linuxを実行する際のオプション
        ip (String): 探索対象のIPアドレス

    Returns:
        String: 実行結果の文字列をそのまま。返す。
        エラーが発生した場合は-1を返す。
    """
    try:
        args = ["enum4linux", option, ip]
        res = subprocess.check_output(args).decode('utf-8')

    except:
        print("enumExecute Error")
        return -1

    return res


def enumGetUserlist(ip):
    """enum4linuxの-Uオプション

    Args:
        ip (_type_): _description_

    Returns:
        _type_: _description_
    """
    res = enumExecute("-U", ip)
    if res == -1:
        return -1

    re_U = r'user:.+'
    userList = re.findall(re_U, res)
    if len(userList) == 0:
        return -1

    return userList


def enumGetSharelist(ip):
    res = enumExecute("-S", ip)
    if res == -1:
        return -1

    re_get_share_start = r'Share Enumeration on .*'
    share_start = re.search(re_get_share_start, res)
    if share_start is None:
        return -1
    res = res[share_start.start():]
    re_get_share_name = r'//.+'
    tmpList = re.findall(re_get_share_name, res)
    if len(tmpList) == 0:
        return -1
    shareList = [x.split('\t')[0] for x in tmpList]
    return shareList


def enumGetOSInfo(ip):
    """enum4linuxの-oオプションで、SMBが動いている環境の情報を取得する。
    OS、SMBのバージョン、その他補足情報を取得。

    Args:
        ip (String): 解析対象のIPアドレス

    Returns:
        dict: 抽出した情報を格納するdict
    """
    # OSInfo_dictに取得した情報を格納する
    OSInfo_dict = {}

    # -oオプションでenum4linuxを実行。正しく実行できなければ終了
    res = enumExecute("-o", ip)
    if res == -1:
        return -1

    # "re_"で始まる変数は正規表現。
    # re_startで、OSなどの情報が載っている部分の開始位置を取得
    re_start = r'Got OS info for .*'
    # re_endで終了位置を取得
    re_end = r'enum4linux complete on .*'
    start = re.search(re_start, res)
    end = re.search(re_end, res)

    # 開始、終了が正しく取得できなかった場合のエラー処理
    if start is None:
        print("enumGetOSInfo: Can not find the beginning of the information")
        return -1

    if end is None:
        print("enumGetOSInfo: Can not find the last of the information")
        return -1

    # 開始から終了まで抽出
    res = res[start.start():end.start()]
    # OSの情報を抽出
    OSInfo_dict['OS'] = res.split('\n')[1]

    # 文字列先頭にカラー情報などが混ざっているので、それを消す処理
    os_find_t = re.search(r'\t', OSInfo_dict['OS'])
    if os_find_t is not None:
        OSInfo_dict['OS'] = OSInfo_dict['OS'][os_find_t.start()+1:]

    # Sambaのバージョン情報を抽出
    re_smb_version = r'\(Samba.*\)'
    find_smb_version = re.search(re_smb_version, OSInfo_dict['OS'])

    # バージョン情報が抜き出せた場合にOSInfo_dictに格納
    if find_smb_version is not None:
        OSInfo_dict['smb_version'] = (find_smb_version.group()
                                      .replace("(", "")
                                      .replace(")", ""))

    # 詳細な情報が書かれている部分を抽出
    # 余計な文字、空欄の削除も一緒に行っている
    re_os_detail = r'.+:.+'
    re_remove_space = r'\s+:'
    res = re.sub(re_remove_space, ":", res.replace("\t", ""))
    osInfoList = re.findall(re_os_detail, res)
    # 今回使った正規表現だとリストに余計な要素が含まれてしまうので、削除している
    osInfoList = osInfoList[1:]
    tmpdict = {x.split(':')[0]: x.split(':')[1]
               for x in osInfoList}
    # 辞書に格納
    OSInfo_dict.update(tmpdict)

    return OSInfo_dict


def enumUsersViaRID(ip):
    ViaRID_dict = {}
    res = enumExecute("-r", ip)

    res_lines = res.split('\n')
    tmp_luser = [x for x in res_lines
                 if "Local User" in x]
    luserList = [x[x.find(' ')+1:] for x in tmp_luser]

    tmp_DGroup = [x for x in res_lines
                  if "Domain Group" in x]
    dgroupList = [x[x.find(' ')+1:] for x in tmp_DGroup]

    tmp_LGroup = [x for x in res_lines
                  if "Local Group" in x]
    lgroupList = [x[x.find(' ')+1:] for x in tmp_LGroup]

    ViaRID_dict['luser'] = luserList
    ViaRID_dict['dgroup'] = dgroupList
    ViaRID_dict['lgroup'] = lgroupList

    return ViaRID_dict


def smbSenario():
    OSInfo_dict = enumGetOSInfo(sys.argv[1])
    print("--- OS Information ---")
    if OSInfo_dict != -1:
        for i, j in OSInfo_dict.items():
            print(i + " : " + j)
    print()
    print("--- User List ---")
    userList = enumGetUserlist(sys.argv[1])
    if userList != -1:
        for i in userList:
            print(i)
    print()
    print("--- Share List ---")
    shareList = enumGetSharelist(sys.argv[1])
    if shareList != -1:
        for i in shareList:
            print(i)
    print()
    print("--- enum Users Via RID ---")
    ViaRID_dict = enumUsersViaRID(sys.argv[1])
    if len(ViaRID_dict["luser"]) != 0:
        print("Local User")
        for i in ViaRID_dict["luser"]:
            print(i)
        print()

    if len(ViaRID_dict["dgroup"]) != 0:
        print("Domain Group")
        for i in ViaRID_dict["dgroup"]:
            print(i)
        print()

    if len(ViaRID_dict["lgroup"]) != 0:
        print("Local Group")
        for i in ViaRID_dict["lgroup"]:
            print(i)


# smbSenario()
