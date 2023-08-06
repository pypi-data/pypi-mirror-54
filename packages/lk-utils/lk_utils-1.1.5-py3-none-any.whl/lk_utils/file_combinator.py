"""
使用方法:
    合并指定目录下的所有 txt 文件, 并在同目录下生成一个 "result.txt" 文件:
        file_combinator.combine_txt(my_dir)
    合并指定目录下的所有 excel 文件, 并在同目录下生成一个 "result.xlsx" 文件:
        file_combinator.combine_excel(my_dir)
    合并指定目录下的所有 csv 文件, 并在同目录下生成一个 "result.xlsx" 文件:
        file_combinator.combine_csv(my_dir)

注意事项:
    如果要生成的 result 文件已存在, 则会被覆盖.
"""
import os

import xlrd

from . import file_sniffer, read_and_write_basic
from .excel_writer import ExcelWriter
from .lk_logger import lk


def combine_txt(idir, trim_header=True):
    sum_file = idir + 'result.txt'
    
    if os.path.exists(sum_file):
        cmd = input('[INFO][file_combinator] the sum file ({}) already exists, '
                    'do you want to overwrite it? (y/n) '.format(sum_file))
        if cmd == 'y':
            pass
        else:
            lk.logt('[I0838]', 'please delete the sum file and retry',
                    h='parent')
            raise AttributeError
    
    files = os.listdir(idir)
    
    writer = read_and_write_basic.FileSword(
        sum_file, 'a', clear_any_existed_content=True)
    
    for f in files:
        if '.txt' in f and f != 'result.txt':
            f = idir + f
            content = read_and_write_basic.read_file(f).strip()
            writer.write(content)
    
    writer.close()
    
    if trim_header:
        from re import compile
        content = read_and_write_basic.read_file(sum_file)
        header = compile(r'^[^\n]+').search(content).group()
        content = content.replace(header + '\n', '')
        content = header + '\n' + content
        read_and_write_basic.write_file(content, sum_file)


def combine_csv(idir='', ofile='result.xls', module=True, ignore=None):
    import csv
    
    if not idir:
        idir = file_sniffer.get_curr_dir()
    else:
        idir = file_sniffer.prettify_dir(idir)
    
    writer = ExcelWriter(idir + ofile)
    header = False
    
    # ----------------------------------------------------------------
    
    files = file_sniffer.find_filenames(idir, '.csv')
    
    for f in files:
        if f == ofile or (ignore and f in ignore):
            continue
        
        lk.logax(f, h='parent')
        
        with open(idir + f, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            
            for index, row in enumerate(spamreader):
                if index == 0:
                    if header:
                        continue
                    else:
                        header = True
                if module:
                    if index == 0:
                        row = ['module'] + row
                    else:
                        row = [f.split('.')[0]] + row
                writer.writeln(*row)
    
    writer.save()


def combine_excel(idir='', ofile='', module=True, ignore=None, one_sheet=True):
    """
    合并指定目录的所有表格文件为一个表格.
    
    ARGS:
        idir: 目标目录, 注意本函数不会处理它的子目录文件
        ofile: 目标输出文件的路径. 为空则表示在 idir 目录下生成一个 result.xlsx
            文件 (PS: 如果 idir 下已有 ofile, 则在合并过程中跳过此文件, 并在最后
            覆盖此文件)
        module: 是否在合并结果中添加一个 "module" 列, 以显示分文件的来源 (文件
            名)
        ignore: None|list|tuple. 需要忽略的文件 (填文件名)
        one_sheet:
            True: 将分文件的数据合并到输出文件的一个 sheet 中. 建议当分文件的字
                段格式相同时使用
            False: 将分文件的数据按照其文件名创建到输出文件的不同 sheet 中. 建议
                (1) 当分文件的字段不同时使用; (2) 当分文件是不同的年份的数据, 我
                们想要按照年份来分放到输出文件的不同 sheet 时使用; (3) 此时建议
                module 参数传 False
    NOTE: ofile 的后缀名只能是 '.xlsx', 即使您传入的是以 '.xls' 结尾
    IN: idir
    OT: ofile
    """
    idir = file_sniffer.prettify_dir(idir) if idir \
        else file_sniffer.get_curr_dir()
    ofile = file_sniffer.prettify_file(ofile) if ofile \
        else idir + 'result.xlsx'
    
    writer = ExcelWriter(ofile, sheetname='' if one_sheet else None)
    header_on = False
    modulex = 0
    
    # prepare files and exclude ignored files
    # NOTE: if ofile in idir, also should be removed from `files`
    files_to_remove = [ofile]
    if ignore:
        files_to_remove.extend((idir + f for f in ignore))
    ifiles = tuple(f for f in file_sniffer.find_filenames(idir, '.xls')
                   if f not in files_to_remove)
    
    for exl in lk.wrap_counter(ifiles):
        modulex += 1
        lk.logax(modulex, exl, h='parent')
        
        filename = exl.split('.', 1)[0]
        
        book = xlrd.open_workbook(idir + exl)
        sheet = book.sheet_by_index(0)
        
        if one_sheet:
            if not header_on:
                header_on = True
                
                if module:
                    header = ['module'] + sheet.row_values(0)
                else:
                    header = sheet.row_values(0)
                
                writer.writeln(*header)
        else:  # 分 sheet 模式
            if module:
                header = ['module'] + sheet.row_values(0)
            else:
                header = sheet.row_values(0)
            
            writer.add_new_sheet(modulex)
            writer.writeln(*header)
            """
            为什么 modulex 不使用 module_name 表示?
                1. excel 的 sheet 命名有长度限制, 不能超过 31 个字符
                2. sheet 命名不能有重名
                3. sheet 命名不能有特殊字符
            因此, 如果用 module name 来命名, 可能会报错. 所以采用安全的做法.
            """
        
        for rowx in range(1, sheet.nrows):
            if module:
                writer.writeln(filename, *sheet.row_values(rowx))
            else:
                writer.writeln(*sheet.row_values(rowx))
    
    writer.save()
