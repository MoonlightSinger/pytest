
# only for windows platforms.
# lower version python path at fist.
# py33 hexversion >= 0x030301f0

pypaths = ["C:\Python32", "C:\Python27"]

# when python hexversion >= 0x030301f0, have python launcher.
pylauncher = False

py3 = True
pypath = ""
pyoldpath = ""

import sys
import os.path
import string

ver = sys.hexversion

if ver < 0x03000000:
    py3 = False
    pypath = pypaths[1]
    pyoldpath = pypaths[0]
    import _winreg as reg
else:  
    py3 = True
    pypath = pypaths[0]
    pyoldpath = pypaths[1]
    import winreg as reg

subkeys_open_py = ["Python.CompiledFile\shell\open\command",
"Python.File\shell\open\command"]
subkey_open_pyw = "Python.NoConFile\shell\open\command"
subkeys_idle = ["Python.File\shell\Edit with IDLE\command",
"Python.NoConFile\shell\Edit with IDLE\command"]
# can not find interactive key.
# #subkeys_interactive = [
# # "Python.File\\shell\\Run in interactive mode\\command",
# # "Python.NoConFile\\shell\\Run in interactive mode\\command"]
subkey_syspath = "SYSTEM\ControlSet001\Control\Session Manager\Environment"
# #C:\Python33\;C:\Tcl\bin;C:\Program Files\NVIDIA Corporation\PhysX\Common;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;C:\Program Files\ATI Technologies\ATI.ACE\Core-Static
subkey_userpath = "Environment"


for subkey in subkeys_open_py:
    with reg.OpenKey(reg.HKEY_CLASSES_ROOT, subkey, 0, reg.KEY_WRITE) as key:
        if pylauncher:
            value = ""
            if py3:
                value = '"{0}\python.exe" "%1" %*'.format(pypath)
            else:
                value = '"C:\WINDOWS\py.exe" "%1" %*'
        else:
            value = '"{0}\python.exe" "%1" %*'.format(pypath)
        reg.SetValueEx(key, None, 0, reg.REG_SZ, value)

    with reg.OpenKey(reg.HKEY_CLASSES_ROOT, subkey_open_pyw, 0, reg.KEY_WRITE) as key:
        if pylauncher:
            value = ""
            if py3:
                value = '"{0}\pythonw.exe" "%1" %*'.format(pypath)
            else:
                value = '"C:\WINDOWS\pyw.exe" "%1" %*'
        else:
            value = '"{0}\python.exe" "%1" %*'.format(pypath)
        reg.SetValueEx(key, None, 0, reg.REG_SZ, value)
print(reg.REG_EXPAND_SZ)
print(sys.hexversion<0x03000000)
for subkey in subkeys_idle:
    with reg.OpenKey(reg.HKEY_CLASSES_ROOT, subkey, 0, reg.KEY_WRITE) as key:
        value = '"{0}\pythonw.exe" "{0}\Lib\idlelib\idle.pyw" -e "%1"'.format(pypath)
        reg.SetValueEx(key, None, 0, reg.REG_SZ, value)

    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, subkey_syspath, 0, reg.KEY_ALL_ACCESS) as key:
        value = reg.QueryValueEx(key, "Path")
        path = ""
        if py3:
            path = value[0].replace(pyoldpath, pypath)
        else:
            path = string.replace(value[0], pyoldpath, pypath)
        reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, path)

    with reg.OpenKey(reg.HKEY_CURRENT_USER, subkey_userpath, 0, reg.KEY_ALL_ACCESS) as key:
        value = reg.QueryValueEx(key, "Path")
        path = ""
        if py3:
            path = value[0].replace(pyoldpath, pypath)
        else:
            path = string.replace(value[0], pyoldpath, pypath)
        reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, path)
