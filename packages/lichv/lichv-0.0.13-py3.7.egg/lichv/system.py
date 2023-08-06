#!/usr/bin/python
# -*- coding: UTF-8 -*-

import platform
import socket
import uuid

class System():
    show_log = True
    hostname = ''

    """docstring for System"""
    def __init__(self):
        super(System, self).__init__()

    def setLogger(self,show=True):
        self.show_log = show
        return self
    
    def get_hostname(self):
    	return socket.gethostname()

    def get_ip(self):
    	return socket.gethostbyname(socket.gethostname())

    def get_platform(self):
        '''获取操作系统名称及版本号'''
        return platform.platform()

    def get_version(self):
        '''获取操作系统版本号'''
        return platform.version()

    def get_architecture(self):
        '''获取操作系统的位数'''
        return platform.architecture()

    def get_machine(self):
        '''计算机类型'''
        return platform.machine()

    def get_node(self):
        '''计算机的网络名称'''
        return platform.node()

    def get_processor(self):
        '''计算机处理器信息'''
        return platform.processor()

    def get_system(self):
        '''获取操作系统类型'''
        return platform.system()

    def get_uname(self):
        '''汇总信息'''
        return platform.uname()

    def get_python_build(self):
        ''' the Python build number and date as strings'''
        return platform.python_build()

    def get_python_compiler(self):
        '''Returns a string identifying the compiler used for compiling Python'''
        return platform.python_compiler()

    def get_python_branch(self):
        '''Returns a string identifying the Python implementation SCM branch'''
        return platform.python_branch()

    def get_python_implementation(self):
        '''Returns a string identifying the Python implementation. Possible return values are: ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’.'''
        return platform.python_implementation()

    def get_python_version(self):
        '''Returns the Python version as string 'major.minor.patchlevel'
        '''
        return platform.python_version()

    def get_python_revision(self):
        '''Returns a string identifying the Python implementation SCM revision.'''
        return platform.python_revision()

    def get_python_version_tuple(self):
        '''Returns the Python version as tuple (major, minor, patchlevel) of strings'''
        return platform.python_version_tuple()

    def get_mac_address(self):
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

    def show_os_all_info(self):
        '''打印os的全部信息'''
        print('获取操作系统名称及版本号 : [{}]'.format(self.get_platform()))
        print('获取操作系统版本号 : [{}]'.format(self.get_version()))
        print('获取操作系统的位数 : [{}]'.format(self.get_architecture()))
        print('计算机类型 : [{}]'.format(self.get_machine()))
        print('计算机的网络名称 : [{}]'.format(self.get_node()))
        print('计算机处理器信息 : [{}]'.format(self.get_processor()))
        print('获取操作系统类型 : [{}]'.format(self.get_system()))
        print('获取操作系统IP地址 : [{}]'.format(self.get_ip()))
        print('获取操作系统MAC地址 : [{}]'.format(self.get_mac_address()))
        print('汇总信息 : [{}]'.format(self.get_uname()))

    def show_os_info(self):
        '''只打印os的信息，没有解释部分'''
        print(self.get_platform())
        print(self.get_version())
        print(self.get_architecture())
        print(self.get_machine())
        print(self.get_node())
        print(self.get_processor())
        print(self.get_system())
        print(self.get_uname())

    def show_python_all_info(self):
        '''打印python的全部信息'''
        print('The Python build number and date as strings : [{}]'.format(self.get_python_build()))
        print('Returns a string identifying the compiler used for compiling Python : [{}]'.format(self.get_python_compiler()))
        print('Returns a string identifying the Python implementation SCM branch : [{}]'.format(self.get_python_branch()))
        print('Returns a string identifying the Python implementation : [{}]'.format(self.get_python_implementation()))
        print('The version of Python ： [{}]'.format(self.get_python_version()))
        print('Python implementation SCM revision : [{}]'.format(self.get_python_revision()))
        print('Python version as tuple : [{}]'.format(self.get_python_version_tuple()))

    def show_python_info(self):
        '''只打印python的信息，没有解释部分'''
        print(self.get_python_build())
        print(self.get_python_compiler())
        print(self.get_python_branch())
        print(self.get_python_implementation())
        print(self.get_python_version())
        print(self.get_python_revision())
        print(self.get_python_version_tuple())
          
    def test(self):
        print('计算机操作系统信息:')
        if self.show_log:
            self.show_os_all_info()
        else:
            self.show_os_info()
        print('#' * 50)
        print('计算机中的python信息：')
        if self.show_log:
            self.show_python_all_info()
        else:
            self.show_python_info()

        print(self.get_hostname())
        print(self.get_ip())
        print(self.get_mac_address())


if __name__ == '__main__':
    system_platform = System()
    system_platform.setLogger(True).test()