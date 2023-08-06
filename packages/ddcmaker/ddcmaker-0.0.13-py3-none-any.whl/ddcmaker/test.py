"""人生若只如初见，何事秋风悲画扇"""
def Authentication_authority(number):
    import subprocess
    cmd = "python3 login_quanxian.pyc --typenum={}".format(number)
    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                # encoding="u8",
                                shell=True)  # 在windows 下运行时为False，linux 下运行为 True
    except Exception as e:
        print(e)
    out, err = proc.communicate(timeout=12)

    # print(out.decode("u8"))
    # print(len(out.decode("u8")))
    if "True" in out.decode("u8"):
        print("验证身份成功")
    else:
        print("验证身份失败")
# Authentication_authority()


