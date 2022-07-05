# -*- coding: utf-8 -*-

import psutil
import collections


disk_used = collections.OrderedDict()

def get_disk_info():
    """
    查看磁盘属性信息
    :return: 磁盘使用率和剩余空间
    """
    for id in psutil.disk_partitions():
        if 'cdrom' in id.opts or id.fstype == '':
            continue
        disk_name = id.device.split(':')
        s = disk_name[0]
        disk_info = psutil.disk_usage(id.device)
        disk_used[s + '盘使用率：'] = '{}%'.format(disk_info.percent)
        disk_used[s + '剩余空间：'] = '{}GB'.format(disk_info.free // 1024 // 1024 // 1024)
    return disk_used


ret = get_disk_info()
for k, v in ret.items():
    print('{}{}'.format(k, v))