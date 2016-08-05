ak = "54bd5bd4a4f2335eb436c938dabcde"
# 下面import代码段写法的原因：
# 1. NUWA_RESOURCES_DIR的数据在django服务启动后，需要一段时间才能就位
# 2. import后需调用setDirPath来加载资源库的metadata.
# 3. 同一进程内的所有请求共享一个nuwa_resources
global nuwa_resources

try:
    import nuwa_resources
except ImportError:
    import sys
    dst_dir = os.getenv('NUWA_RESOURCES_DIR')
    sys.path.append(dst_dir)
    import nuwa_resources
    nuwa_resources.setDirPath(ak, dst_dir)
    # print "total: ", nuwa_resources.totalNum(ak)
    # read
