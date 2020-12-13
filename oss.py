import oss2
import sys
import os

auth = oss2.Auth('ID','KeySecret')
py_file_path=sys.path[0]
bucket = oss2.Bucket(auth,'oss-cn-where.aliyuncs.com','bucket_name')
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def upload_file(uploadName,filename):
    bucket.put_object_from_file(str(uploadName),str(filename),progress_callback=percentage)


def find_new_file(dir):
    '''查找目录下最新的文件'''
    file_lists = os.listdir(dir)
    new_file_lists=[]
    for files_check1 in file_lists:
        if files_check1.endswith('xxx'):
            new_file_lists.append(files_check1)
        else:
            pass
    new_file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn)
                    if not os.path.isdir(dir + "\\" + fn) else 0)
    #print('最新的文件为： ' + file_lists[-1])
    file = os.path.join(dir, new_file_lists[-1])
    #print('完整路径：', file)
    return file,new_file_lists[-1]


file_check_root=[]
for root,dirs,files in os.walk(py_file_path):
    #print('root: '+root,' dirs: '+dirs,' files: '+files) dirs为所有文件夹，files为所有文件
    for i in files:
        #print('files: '+i)
        #sys.stdout.flush()
        if i.endswith('xxx'):
            if not root in file_check_root:
                new_file_root=find_new_file(root)
                #print(new_file_root[0])
                #sys.stdout.flush()
                file_check_root.append(root)
                filename=os.path.join(root,new_file_root[1])
                upload_file(new_file_root[1],filename)
            else:
                pass
            #upload_file(i,filename)
        else:
            continue
