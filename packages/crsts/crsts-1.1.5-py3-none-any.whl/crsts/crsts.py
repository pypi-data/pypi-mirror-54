import os
import time
import hashlib
import shutil
import pickle
import base64
from multiprocessing import Process, JoinableQueue
import subprocess

def write2path(lines,path,encoding='utf-8',method='lines',append='w'):
    with open(path,append,encoding=encoding) as fw:
        if method=='lines':
            fw.writelines(lines)
        else:
            fw.write(lines)

def read_path(path,method='readlines',encoding='utf-8',errors='strict'):
    with open(path,'r',encoding=encoding,errors=errors) as fr:
        if method == "readlines":
            all_lines = fr.readlines()
        else:
            all_lines = fr.read()
        return all_lines

def print_list(array,index=False):
    if index:
        for i,val in enumerate(array):
            print(i,val)
    else:
        for val in array:
            print(val)

def get_top_n_files(folder_path,n):
    if not os.path.exists(folder_path):
        print('源文件夹不存在.')
        return []
    if folder_path[-1] != '/':
        folder_path=folder_path+'/'
    top_n_files = [folder_path+f for f in os.listdir(folder_path)[:n]]
    return top_n_files

def copy_top_n_file(folder_path,n,dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    top_n_files = get_top_n_files(folder_path,n)
    for f in top_n_files:
        copyfile(f,dst_folder)

def save2pkl(obj,path,protocol=-1):
    with open(path,'wb') as fw:
        pickle.dump(obj,fw,protocol=protocol)

def read_pkl(path):
    with open(path, 'rb') as fr:
        obj = pickle.load(fr)
        return obj

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def getTimeSpan(begin_time, end_time, format='minute'):
    # 获取2个字串串格式的时间差
    begin_time = time.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
    end_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    begin_timeStamp = int(time.mktime(begin_time))
    end_timeStamp = int(time.mktime(end_time))
    span_seconds = abs(end_timeStamp - begin_timeStamp)

    if format == 'second':
        return int(round(span_seconds, 2))
    elif format == 'minute':
        return int(round(span_seconds / 60, 2))
    elif format == 'hour':
        return int(round(span_seconds / 3600, 2))
    elif format == 'day':
        return int(round(span_seconds / 86400, 2))
    else:
        return int(round(span_seconds, 2))

def get_file_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5

def getfilesize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / (1000 * 1000)
    return round(fsize, 2)

def listDir(rootDir):
    list_filepath = []
    for filename in os.listdir(rootDir):
        pathname = os.path.join(rootDir, filename)
        if os.path.isfile(pathname):
            list_filepath.append(pathname)
    return list_filepath

def makedir(dir_path,delete_exists=False):
    if os.path.exists(dir_path):
        if delete_exists:
            rmfolder(dir_path)
            os.makedirs(dir_path)
        else:
            print("--------创建文件夹失败:" + dir_path + ",路径已存在--------")
    else:
        os.makedirs(dir_path)

def touchfile(path):
    if not os.path.exists(path):
        f = open(path,'w')
        f.close()

def copyfile(origin_path, target_path):
    if os.path.isfile(origin_path):
        shutil.copy(origin_path, target_path)
    else:
        print("--------复制文件失败:" + origin_path + ",路径不存在--------")

def movefile(origin_path, target_path):
    if os.path.isfile(origin_path):
        shutil.move(origin_path, target_path)
    else:
        print("--------移动文件失败:" + origin_path + ",路径不存在--------")

def copyfolder(origin_folder, target_folder, *args):
    # 目标文件夹名为 target_path，不能已经存在；方法会自动创建目标文件夹。
    if os.path.isdir(origin_folder):
        shutil.copytree(origin_folder, target_folder, ignore=shutil.ignore_patterns(*args))
    else:
        print("--------复制文件夹失败:" + origin_folder + ",路径不存在--------")

def rmfile(del_file):
    if os.path.isfile(del_file):
        os.remove(del_file)
    else:
        print("--------删除文件失败:" + del_file + ",路径不存在--------")

def rmfolder(del_folder):
    if os.path.isdir(del_folder):
        shutil.rmtree(del_folder)
    else:
        print("--------删除文件夹失败:" + del_folder + ",路径不存在--------")

def base64decode(strings,encoding='utf-8'):
    try:
        base64_decrypt = base64.b64decode(strings.encode('utf-8'))
        return str(base64_decrypt, encoding)
    except:
        return ''

def base64encode(strings,encoding='utf-8'):
    try:
        base64_encrypt = base64.b64encode(strings.encode('utf-8'))
        return str(base64_encrypt, encoding)
    except:
        return ''

def run_cmd(cmd,with_output=False):
    if with_output:
        return subprocess.getstatusoutput(cmd)
    else:
        return subprocess.call(cmd, shell=True)

def run_multi_task(all_items,done_path,user_func,cpu_num=os.cpu_count()):
    begin_time = time.time()
    touchfile(done_path)
    done_items = [f.strip() for f in read_path(done_path)]
    undone_items = list(set(all_items) - set(done_items))
    print(f'检测到全部:{len(all_items)}个')
    print(f'检测到已完成的:{len(done_items)}个')
    print(f'重新计算需要处理的个数为:{len(undone_items)}个')
    print(f'启动{cpu_num}个进程,开始运行')

    q = JoinableQueue()
    for item in undone_items:
        q.put(item)

    def func_task(q):
        while True:
            item = q.get()
            user_func(item)
            write2path(item+'\n',done_path,method='line',append='a')
            q.task_done()

    for i in range(cpu_num):
        p = Process(target=func_task, args=(q,))
        p.daemon = True
        p.start()
    q.join()
    print(f'全部已完成，用时:{int(time.time() - begin_time)}')





