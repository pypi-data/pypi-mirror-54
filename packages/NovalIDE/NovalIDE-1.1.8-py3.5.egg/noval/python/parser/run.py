from __future__ import print_function
import sys
import os
import pickle
import config,fileparser,utils
import json
import types
import time
import functools
import multiprocessing
import datetime

def generate_builtin_data(dest_path):
    def make_python2_builtin_types(builtin_type,recursive=True):
        childs = []
        for name in dir(builtin_type):
            try:
                builtin_attr_intance = getattr(builtin_type,name)
            except:
                continue
            builtin_attr_type = type(builtin_attr_intance)
            if builtin_attr_type == types.TypeType:
                if not recursive:
                    continue
                builtin_attr_childs = make_python2_builtin_types(builtin_attr_intance,False)
                node = dict(name = name,is_builtin=True,type = config.NODE_CLASSDEF_TYPE,childs=builtin_attr_childs,doc=builtin_attr_intance.__doc__)
                childs.append(node)
            elif builtin_attr_type == types.BuiltinFunctionType or builtin_attr_type == types.BuiltinMethodType \
                        or str(builtin_attr_type).find("method_descriptor") != -1:
                node = dict(name = name,is_builtin=True,type = config.NODE_FUNCDEF_TYPE,doc=builtin_attr_intance.__doc__)
                childs.append(node)
            else:
                node = dict(name = name,is_builtin=True,type = config.NODE_OBJECT_PROPERTY)
                childs.append(node)
        return childs

    def make_python3_builtin_types(builtin_type,recursive=True):
        childs = []
        for name in dir(builtin_type):
            try:
                builtin_attr_intance = getattr(builtin_type,name)
            except:
                continue
            builtin_attr_type = type(builtin_attr_intance)
            if builtin_attr_type == type(type):
                if not recursive:
                    continue
                builtin_attr_childs = make_python3_builtin_types(builtin_attr_intance,False)
                node = dict(name = name,is_builtin=True,type = config.NODE_CLASSDEF_TYPE,childs=builtin_attr_childs,doc=builtin_attr_intance.__doc__)
                childs.append(node)
            elif builtin_attr_type == types.BuiltinFunctionType or builtin_attr_type == types.BuiltinMethodType \
                        or str(builtin_attr_type).find("method_descriptor") != -1:
                node = dict(name = name,is_builtin=True,type = config.NODE_FUNCDEF_TYPE,doc=builtin_attr_intance.__doc__)
                childs.append(node)
            else:
                node = dict(name = name,is_builtin=True,type = config.NODE_OBJECT_PROPERTY)
                childs.append(node)
        return childs

    def make_builtin_types(builtin_type):
        if utils.IsPython2():
            return make_python2_builtin_types(builtin_type)
        else:
            return make_python3_builtin_types(builtin_type)
        
    dest_path = os.path.join(dest_path,"builtins")
    utils.MakeDirs(dest_path)
    for built_module in sys.builtin_module_names:
        module_instance = __import__(built_module)
        childs = make_builtin_types(module_instance)
        with open(dest_path + "/" + built_module + config.MEMBERLIST_FILE_EXTENSION, 'w') as f:
            for node in childs:
                f.write(node['name'])
                f.write('\n')
        module_dict = fileparser.make_module_dict(built_module,'',True,childs,doc=module_instance.__doc__)
        with open(dest_path + "/" + built_module + config.MEMBERS_FILE_EXTENSION, 'wb') as j:
            # Pickle dictionary using protocol 0.
            pickle.dump(module_dict, j,protocol=0)
            
def LoadDatabaseVersion(database_location):
    with open(os.path.join(database_location,config.DATABASE_FILE)) as f:
        return f.read()
        
def SaveDatabaseVersion(database_location,new_database_version):
    with open(os.path.join(database_location,config.DATABASE_FILE),"w") as f:
        f.write(new_database_version)
        
def SaveLastUpdateTime(database_location):
    with open(os.path.join(database_location,config.UPDATE_FILE),"w") as f:
        datetime_str = datetime.datetime.strftime(datetime.datetime.now(), config.ISO_8601_DATETIME_FORMAT)
        f.write(datetime_str)
        
def NeedRenewDatabase(database_location,new_database_version):
    if not os.path.exists(os.path.join(database_location,config.DATABASE_FILE)):
        return True
    old_database_version = LoadDatabaseVersion(database_location)
    if 0 == utils.CompareCommonVersion(new_database_version,old_database_version):
        return False
    return True

def get_python_version():
    #less then python 2.7 version
    if isinstance(sys.version_info,tuple) and sys.version_info[0] == 2:
        version = str(sys.version_info[0]) + "." +  str(sys.version_info[1]) 
        #if sys.verion[0] == 2 and sys.version_info[2] > 0:
        if sys.version_info[2] > 0:
            version += "."
            version += str(sys.version_info[2])
    #python 2.7 or python3 version,which python3 version type is tuple,python2.7 version type is not tuple
    else:
        if sys.version_info.releaselevel.find('final') != -1:
            version = str(sys.version_info.major) + "." +  str(sys.version_info.minor) + "."  + str(sys.version_info.micro)
        elif sys.version_info.releaselevel.find('beta') != -1:
            version = str(sys.version_info.major) + "." +  str(sys.version_info.minor) + "."  + str(sys.version_info.micro) + \
                        "b" + str(sys.version_info.serial)
        elif sys.version_info.releaselevel.find('candidate') != -1:
            version = str(sys.version_info.major) + "." +  str(sys.version_info.minor) + "."  + str(sys.version_info.micro) + \
                    "rc" +  str(sys.version_info.serial)
        elif sys.version_info.releaselevel.find('alpha') != -1:
            version = str(sys.version_info.major) + "." +  str(sys.version_info.minor) + "."  + str(sys.version_info.micro) + \
                "a" + str(sys.version_info.serial)
        else:
            print (sys.version_info.releaselevel)
    return version
     
def generate_intelligent_data_by_pool(out_path,new_database_version):
    version = get_python_version()
    dest_path = os.path.join(out_path,version)
    utils.MakeDirs(dest_path)
    need_renew_database = NeedRenewDatabase(dest_path,new_database_version)
    sys_path_list = sys.path
    max_pool_count = 5
    for i,path in enumerate(sys_path_list):
        sys_path_list[i] = os.path.abspath(path)
    pool = multiprocessing.Pool(processes=min(max_pool_count,len(sys_path_list)))
    future_list = []
    for path in sys_path_list:
        print ('start parse path data',path)
        pool.apply_async(scan_sys_path,(path,dest_path,need_renew_database))
    pool.close()
    pool.join()
    process_sys_modules(dest_path)
    if need_renew_database:
        SaveDatabaseVersion(dest_path,new_database_version)
    SaveLastUpdateTime(dest_path)
    
def get_unfinished_modules(outpath):
    unfinished_file_name = "unfinish.txt"
    unfinished_file_path = os.path.join(outpath,unfinished_file_name)
    if not os.path.exists(unfinished_file_path):
        return []
    module_paths = []
    try:
        with open(unfinished_file_path) as f:
            module_paths = f.read().split()
        os.remove(unfinished_file_path)
    except:
        pass
    return module_paths
     
def scan_sys_path(src_path,dest_path,need_renew_database):

    def is_path_ignored(path):
        for ignore_path in ignore_path_list:
            if path.startswith(ignore_path):
                return True
        return False
    ignore_path_list = []
    unfinished_module_paths = get_unfinished_modules(os.path.dirname(dest_path))
    for root,path,files in os.walk(src_path):
        if is_path_ignored(root):
            continue
        if root != src_path and is_test_dir(root):
            ignore_path_list.append(root)
          ##  print ('path',root,'is a test dir')
            continue
        elif root != src_path and not fileparser.is_package_dir(root):
            ignore_path_list.append(root)
           ### print ('path',root,'is not a package dir')
            continue
        for afile in files:
            fullpath = os.path.join(root,afile)
            ext = os.path.splitext(fullpath)[1].lower()
            if not ext in ['.py','.pyw']:
                continue
            is_file_unfinished =  fullpath in unfinished_module_paths
            file_need_renew_database = need_renew_database or is_file_unfinished
            file_parser = fileparser.FiledumpParser(fullpath,dest_path,force_update=file_need_renew_database)
            file_parser.Dump()
           
def is_test_dir(dir_path):
    dir_name = os.path.basename(dir_path)
    if dir_name.lower() == "test" or dir_name.lower() == "tests":
        return True
    else:
        return False


def process_sys_modules(dest_path):
    for name in list(sys.modules.keys()):
        module_members_file = os.path.join(dest_path,name+ config.MEMBERS_FILE_EXTENSION)
        if os.path.exists(module_members_file):
            ###print 'sys module',name,'has been already analyzed'
            continue
        if not hasattr(sys.modules[name],'__file__'):
            continue
        fullpath = sys.modules[name].__file__.rstrip("c")
        if not fullpath.endswith(".py"):
            continue

        file_parser = fileparser.FiledumpParser(fullpath,dest_path)
        file_parser.Dump()
        

def generate_intelligent_data(out_path,new_database_version):
    version = get_python_version()
    dest_path = os.path.join(out_path,version)
    utils.MakeDirs(dest_path)
    need_renew_database = NeedRenewDatabase(dest_path,new_database_version)
    sys_path_list = sys.path
    for i,path in enumerate(sys_path_list):
        sys_path_list[i] = os.path.abspath(path)
    for path in sys_path_list:
        print ('start parse path data',path)
        scan_sys_path(path,dest_path,need_renew_database)
    process_sys_modules(dest_path)
    if need_renew_database:
        SaveDatabaseVersion(dest_path,new_database_version)
    
if __name__ == "__main__":
    ###generate_builtin_data("./")
    start_time = time.time()
    out_path = sys.argv[1]
    new_database_version = sys.argv[2]
    #generate_intelligent_data(out_path,new_database_version)
    generate_intelligent_data_by_pool(out_path,new_database_version)
    end_time = time.time()
    elapse = end_time - start_time
    print ('elapse time:',elapse,'s')
    print ('end............')