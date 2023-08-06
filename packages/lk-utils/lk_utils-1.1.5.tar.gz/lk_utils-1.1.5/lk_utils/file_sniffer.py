from os import environ, listdir, path as ospath, walk
from sys import argv, path as syspath


# ------------------------------------------------ path trickers

def prettify_dir(adir: str) -> str:
    if '\\' in adir:
        adir = adir.replace('\\', '/')
    if adir[-1] != '/':
        adir += '/'
    return adir


def prettify_file(afile: str) -> str:
    if '\\' in afile:
        afile = afile.replace('\\', '/')
    return afile


def get_dirname(adir: str):
    return adir.strip('/').rsplit('/', 1)[-1]


def get_filename(file, include_suffix=True):
    file = prettify_file(file)
    if '/' not in file and '.' not in file:
        return file
    
    if '/' in file:
        filename = ospath.split(file)[1]
    else:
        filename = file
    
    if not include_suffix:
        filename = ospath.splitext(filename)[0]
    
    return filename


# ------------------------------------------------ path getters

def get_lkdb_path():
    # NOTE: this is an environmental path.
    return prettify_dir(environ['LKDB'])


def get_launch_path():
    path = ospath.abspath(argv[0])
    return prettify_file(path)


def get_curr_dir() -> str:
    """
    IN: get_launch_path()
            获得启动文件的绝对路径, e.g. 'D:workspace/my_project/launcher.py'
    OT: 返回启动文件所在的目录. e.g. 'D:workspace/my_project/'
    """
    adir = ospath.split(get_launch_path())[0]
    """
    get_launch_path() = 'D:workspace/my_project/launcher.py'
    --> ospath.split(get_launch_path()) = [
            'D:workspace/my_project',
            'launcher.py'
        ]
    --> ospath.split(get_launch_path())[0] = 'D:workspace/my_project'
    """
    return prettify_dir(adir)


curr_dir = get_curr_dir()


# ------------------------------------------------ path finders

def find_files(adir, suffix='', rtype='filepath'):
    """
    ARGS:
        adir (str)
        suffix (str, tuple, list): 后缀名必须以 '.' 开头. 例如 '.jpg' 或
            ['.jpg', '.png'] 等
            suffix 针对不同类型的数值, 采用的策略是不同的. 有如下注意事项:
                如果 suffix 类型为 str, 则 suffix 采用的是 "模糊" 查找策略 -- 只
                要文件名中包含 suffix 就能被查找到. 比如 suffix = '.xls', 会同时
                找到 '.xls' 和 '.xlsx' 的文件; 比如 suffix = '.htm', 会同时找到
                '.htm' 和 '.html' 的文件. 这在大多数情况下是既正确又方便的.
                但 "模糊" 查找也带来了很多不确定性, 例如, 当文件中混有 'xlsx' 和
                'xlsm' (excel 模板文件) 时, 后者也会被包含进来; 此外 '.jpg' 也无
                法关联查找到 '.jpeg' (因为二者的字符串并非 "包含" 关系, 且基于效
                益考虑, 此类关联不会被支持); 而且 '.xlsx' 向 '.xls' 的关联查找也
                是不行的; 此外, 一种比较罕见的情况是, 如果有文件名为
                'A.jpg.txt', 那么也会被 suffix = '.jpg' 接纳... 因此, 如果您需要
                更确定的查找结果, 应使用 list 或 tuple类型.
                当 suffix 类型为 list 或 tuple 时, 使用的是精确查找. 比如
                ['.xls'] 的返回结果不会包含除 '.xls' 以外的文件.
                因此, 请根据需要确定需要哪种方式. 在大多数情况下, 我们建议您使用
                str 类型, 因为它使用便捷, 写法简洁, 且适应大多数的情况.
        rtype (str, int): 'filepath'(0)|'filename'(1)|'dict'(2)|'list'(3)
            'filepath': 返回完整路径. e.g. ['D:/A/B.txt', 'D:/A/C.txt']
            'filename': 返回文件名. e.g. ['B.txt', 'C.txt']
            'dict': 返回 {filename: filepath} 格式. e.g. {'B.txt': 'D:/A/B.txt',
                'C.txt': 'D:/A/C.txt'}
            'list': 返回 (filepaths, filenames) 格式. e.g. (['D:/A/B.txt',
                'D:/A/C.txt'], ['B.txt', 'C.txt'])
            此外, 为了简化写法, 我们提供了另外两种方案:
                1. rtype 允许传入数字 0, 1, 2, 3 分别代表这四个值
                2. 如果只想返回文件名 (rtype=1), 可以改用 find_filenames() 方法
    """
    if isinstance(rtype, int):
        rtype = ('filepath', 'filename', 'dict', 'list')[rtype]
    
    adir = prettify_dir(adir)
    all_files = [x for x in listdir(adir) if ospath.isfile(adir + x)]
    
    if suffix:
        if isinstance(suffix, str):
            filenames = [x for x in all_files if suffix in x]
        else:  # type tuple | list
            filenames = [x for x in all_files
                         if ospath.splitext(x)[1].lower() in suffix]
    else:
        filenames = all_files
    
    if rtype == 'filename':
        return filenames
    filepaths = [adir + x for x in filenames]
    if rtype == 'filepath':
        return filepaths
    if rtype == 'dict':
        return dict(zip(filenames, filepaths))
    if rtype == 'list':
        return filepaths, filenames
    
    raise AttributeError  # unknown rtype value


def find_filenames(adir, suffix=''):
    return find_files(adir, suffix, 'filename')


def findall_files(main_dir: str) -> list:
    collector = []
    
    for root, dirs, files in walk(main_dir):
        root = prettify_dir(root)
        collector.extend([root + f for f in files])
    
    return collector


def find_subdirs(main_dir, return_full_path=True,
                 except_protected_folder=True) -> list:
    """
    ARGS:
        main_dir: 入口目录
        return_full_path: 返回完整路径
        except_protected_folder: 排除受保护的文件夹. 当启用时, 对以 "." 或 "__"
            开头的文件夹排除 (例如 ".git", ".idea", "__pycache__").
    """
    paths = listdir(main_dir)
    if except_protected_folder:
        paths = filter(
            lambda x: not (x.startswith('.') or x.startswith('__')), paths
        )
    paths = filter(lambda x: ospath.isdir(main_dir + x), paths)
    if return_full_path:
        return [main_dir + x + '/' for x in paths]
    else:
        return list(paths)


def findall_subdirs(main_dir: str, except_protected_folder=True) -> list:
    """
    refer: https://www.cnblogs.com/bigtreei/p/9316369.html
    """
    collector = []
    
    def my_filter(x: str):
        if except_protected_folder:
            return not (x.startswith('.') or x.startswith('__'))
        else:
            return True
    
    for root, dirs, files in walk(main_dir):
        root = prettify_dir(root)
        collector.extend(root + d for d in filter(my_filter, dirs))
    
    return collector


def find_project_dir(custom_working_entrance=''):
    """
    注: 当从 pycharm 启动时, 项目路径就是 syspath 的第二个元素 (syspath[1]); 当
    从 cmd 或者 pyinstaller 导出后的 exe 启动时, 项目路径就是当前文件所在的路径.
    如果您想要自定义项目路径, 请在启动脚本的顶部加入此代码片段:
        # test.py
        from lk_utils import file_sniffer
        file_sniffer.curr_project_dir = file_sniffer.find_project_dir(
            file_sniffer.curr_dir
        )
        # 或者
        file_sniffer.curr_project_dir = file_sniffer.find_project_dir(
            file_sniffer.get_relpath(__file__, '.')
        )
        
    """
    if custom_working_entrance:
        p = ospath.abspath(custom_working_entrance)
        if p not in syspath:
            syspath.insert(1, p)
    
    assume_project_dir = prettify_dir(syspath[1])
    
    if assume_project_dir in curr_dir:
        """
        assume_project_dir = 'D:/likianta/workspace/myprj/'
        curr_dir = 'D:/likianta/workspace/myprj/src/'
        """
        return assume_project_dir
    else:
        return curr_dir


curr_project_dir = find_project_dir()


# ------------------------------------------------ quicks

def isfile(filepath: str) -> bool:
    """
    一个不是很可靠的方法, 判断是否 (看起来像是) 文件路径.
    
    与 os.path.isfile 不同的地方在于, 本方法允许使用未存在的 filepath. 换句话说,
    本函数只检测 filepath 是不是 "看起来像" 文件, 并不保证一定能判断准确 (比如在
    文件夹名称中带点号就会误判).
    虽然本方法不能保证百分百正确, 但应对常见的情况足够了. 同时, 本方法也会尽可能
    保证检测的效率.
    
    如何加速判断: 使 filepath 的字符串以 '/' 结尾
    """
    if ospath.exists(filepath):
        return ospath.isfile(filepath)
    
    if filepath.endswith('/'):
        return False
    elif '.' in filepath.rsplit('/', 1)[1]:
        return True
    else:
        return False


def isdir(dirpath: str) -> bool:
    if dirpath in ('.', './', '/'):
        return True
    else:
        return not isfile(dirpath)


def getpath(path: str):
    """
    快速地获取文件路径. 返回的是绝对路径.
    
    使用方法见 
        https://blog.csdn.net/Likianta/article/details/89299937#20190414185549
    
    注: path 参数填相对于项目根路径的路径.
    """
    if path.startswith('../'):
        path = path.replace('../', '')
    elif path.startswith('./'):
        path = path[2:]
    return curr_project_dir + path


def get_relpath(a, b):
    """
    已知绝对路径 a, 求 "相对距离" 为 b 的某一路径.

    IO: a                           | b         | out
        'D:/workspace/myprj/A/B.py' | '../'     | 'D:/workspace/myprj/'
        'D:/workspace/myprj/A/B.py' | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/'     | 'C/D/'    | 'D:/workspace/myprj/A/C/D/'
        'D:/workspace/myprj/A/B.py' | '../C/D/' | 'D:/workspace/myprj/C/D/'
    """
    if isfile(a):
        a = ospath.split(a)[0]
    
    if b in ('', '.', './'):
        return prettify_dir(a)
    
    if isfile(b):
        return prettify_file(ospath.abspath(ospath.join(a, b)))
    else:
        return prettify_dir(ospath.abspath(ospath.join(a, b)))


# ------------------------------------------------ interactive

def dialog(adir, suffix, prompt='请选择您所需文件的对应序号') -> str:
    """
    文件对话框.
    NOTE: 本函数不建议使用 lk_logger.
    IN: 要查看的文件夹和该文件夹下的指定后缀的文件
    OT: 指定的文件的绝对路径
    """
    if not prompt.endswith(': '):
        prompt += ': '
    print(f'当前目录为: {adir}')
    
    # fp: filepaths, fn: filenames
    fp, fn = find_files(adir, suffix, 'list')
    
    if not fn:
        print('[WARNING] 当前目录没有找到表格类型的文件')
        return ''
    
    elif len(fn) == 1:
        print(f'当前目录找到了一个目标类型的文件: {fn[0]}')
        return fp[0]
    
    else:
        x = ['{} | {}'.format(i, j) for i, j in enumerate(fn)]
        print('当前目录找到了多个目标类型的文件:\n\t{}'.format('\n\t'.join(x)))
        
        index = input(prompt)
        return fp[int(index)]
