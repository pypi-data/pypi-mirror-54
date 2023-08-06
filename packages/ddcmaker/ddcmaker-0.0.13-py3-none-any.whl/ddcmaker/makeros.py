import json
import subprocess
import time
import os
import base64


def linux_maker(data, settime=60, offline_running=False):
    res = {"msg": "", "code": 1, "data": {}}

    # print(data)
    # data = json.loads(request)
    # print(type(data))

    data = str(data, encoding="u8").replace('    ', '')
    # print(data)
    if not data:
        res.update(err="代码不能为空，请输入代码。")
        return json.dumps(res)
    try:
        code = eval(data)["code"]
        code = base64.b64decode(code)
        code = str(code, encoding="u8").replace('    ', '')
        # print("取出传入的值", code)
    except Exception as e:
        # print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    if code == "":
        res.update(err="代码不能为空，请输入代码。")
        # print(type(res))
        return json.dumps(res)
    if code != "" and "stop" in code[:15]:
        # 终止机器人运动的函数
        typeint = eval(data)["type"]
        if typeint == 0:
            import ddcmaker
            robot = ddcmaker.Robot()
            robot.up()
        elif typeint == 1:
            import ddcmaker
            car = ddcmaker.Car()
            car.stop()
        else:
            print("没有对应创客设备！")
        res.update(code=666, msg="动作已经终止", err="前端请求主动中断动作，杀死运行进程。")
        return json.dumps(res)
    # fp, file_name = mkstemp(suffix=".py", text=True)
    pyname = str(time.time())[-6:] + ".py"
    file_name = "resave//" + pyname
    # print(file_name)
    # print(code)
    if "###offline_running=True###" in code[:50]:
        offline_running = True
    with open(file_name, "w+", encoding="u8") as f:
        # print(type(code))
        f.write(code)
        f.close()

    # cmd = "python3 -IB  "+file_name  # 在linux 下运行为python3

    cmd = "python3  " + file_name
    if offline_running != True:
    #============代码检查============
        ff = open(file_name, "r", encoding="u8")
        ad = ff.readlines()
        # print(ad)
        unsafename = "os"
        for line in ad:
            ss = line.split("import")
            if len(ss) > 1:
                now_list = ss[1].split(unsafename)
                if len(now_list) > 1:
                    res.update(code=555, msg="安全检查未通过",
                               err="代码中引入了" + unsafename + "库，违反了机器人第三定律，终止运行，请检查代码后重新运行")
                    os.remove(file_name)
                    return json.dumps(res)

    #==========代码检查=============

        try:
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    # encoding="u8",
                                    shell=True)  # 在windows 下运行时为False，linux 下运行为 True
        except Exception as e:
            res.update(err=e)
            # print(type(res))
            return json.dumps(res)
        # settime = 60
        try:
            out, err = proc.communicate(timeout=settime)
        except:
            # proc.kill()
            makername = ""
            if os.path.exists('/home/pi/human') == True or os.path.exists('/home/pi/human_code') == True :
                from ddcmaker import killprocess
                killprocess.kill_process(pyname)
                makername = "机器人"
            if os.path.exists('/home/pi/Car') == True:
                import ddcmaker
                car = ddcmaker.Car()
                car.stop()
                makername = "无人车"

            res.update(code=233, msg="超时主动中断",
                       err="运行超时，中断" + makername + "操作，" + makername + "一次最长允许运行动作" + str(settime) + "秒")
        else:
            if err:
                res.update(err=err.decode("u8"))
            else:
                res.update(code=0, msg="执行成功", data={
                    "moduleData": [out.decode("u8")],
                    "printData": out.decode("u8"),
                })
        finally:
            # os.close(fp)
            os.remove(file_name)
        # print(res)
        return json.dumps(res)
    else:
        print("当前设备脱机运行，不再受到平台约束！")
        res.update(code=777, msg="高级模式脱机运行",
                   err="警告：当前模式为高级模式，设备将执行脱机命令，设备将不会超时中断动作！\n请谨慎使用，仅限教师或者工程师调试使用！！\n若要停止，请等待设备运行结束或者关闭设备电源")

        def tuojires():
            try:
                proc = subprocess.Popen(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 # encoding="u8",
                                 shell=True)  # 在windows 下运行时为False，linux 下运行为 True
                proc.communicate(timeout=1000)
            except Exception as error:
                print(error)
            finally:
                os.remove(file_name)
        import threading
        th1 = threading.Thread(target=tuojires)
        th1.setDaemon(True)
        th1.start()
        return json.dumps(res)

def windows_maker(data):
    res = {"msg": "", "code": 1, "data": {}}
    # print(data)
    # data = json.loads(request)
    # print(type(data))

    data = str(data, encoding="u8").replace('    ', '')
    print(data)
    try:
        code = eval(data)["code"]
        code = base64.b64decode(code)
        code = str(code, encoding="u8").replace('    ', '')
        print("取出传入的值", code)
    except Exception as e:
        print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    if code == "":
        res.update(err="代码不能为空，请输入代码。")
        # print(type(res))
        return json.dumps(res)
    if code != "" and "stop" in code[:15]:
        # 终止机器人运动的函数
        print("终止机器人运动")
        res.update(code=666, msg="动作已经终止", err="前端请求主动中断动作，杀死运行进程。")
        return json.dumps(res)
    # fp, file_name = mkstemp(suffix=".py", text=True)
    file_name = str(time.time())[-6:] + ".py"
    print(file_name)
    with open(file_name, "w+", encoding="u8") as f:
        # print(type(code))
        f.write(code)
        f.close()
    # print()
    # cmd = "python3 -IB  "+file_name  # 在linux 下运行为python3
    cmd = "python " + file_name
    print(cmd)
    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="u8",
                                shell=False)  # 在windows 下运行时为False，linux 下运行为 True
    except Exception as e:
        print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    try:
        out, err = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        res.update(code=233, msg="机器运行超时，中断机器人链接。")
    else:
        if err:
            res.update(err=err)
        else:
            res.update(code=0, data={
                "moduleData": [out],
                "printData": out,
            })
    finally:
        # os.close(fp)
        os.remove(file_name)
    return json.dumps(res)


def Mac_maker():
    res = {"msg": "", "code": 1, "data": {}}
    res.update(err="当前系统为Mac,暂时不支持此系统！")
    return json.dumps(res)


def other_maker():
    res = {"msg": "", "code": 1, "data": {}}
    res.update(err="你这是啥系统呀，暂时不支持哟！")
    return json.dumps(res)
