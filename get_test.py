#coding=utf8
# 将目录下面的py文件重命名，然后复制到本目录下

target_path = '/Users/hwf/Documents/work/tools/codeql-home/vscode-codeql-starter/ql/python/ql/test'

def list_all_files(rootdir):
    import os
    _files = []

    list_file = os.listdir(rootdir)
    for i in range(0,len(list_file)):
        path = os.path.join(rootdir,list_file[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files

files=list_all_files(target_path)
# files = [x.replace(target_path+"/","").replace("/","_") for x in files if x.endswith(".py")]
# print("\n".join(files))

def copy_file(files):
    target_prefix = "./office_example/"
    from shutil import copyfile
    for filename in files:
        if filename.endswith(".py"):
            target_file = target_prefix+filename.replace(target_path+"/","").replace("/","_")
            copyfile(filename,target_file)
            print("[debug] finished {} -> {}".format(filename,target_file))

copy_file(files)