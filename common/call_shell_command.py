import subprocess
def reload_data():
    cmd = 'python /code/scripts/reset_data_in_redis.py'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  

    if sync_block:  # 等命令执行完
        for line in p.stdout.readlines():  
            app.logger.info(line)
        p.wait()  
        if p.returncode != 0:
            app.logger.error("return code: %s" % p.returncode)
            raise Exception('callCommand error. cmd: '+cmd)
    else:          # 不等命令执行完
        pass

