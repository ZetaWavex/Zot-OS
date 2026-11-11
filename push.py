import time
import os

t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cmd = f'git commit -m "Update {t}"'

print("程序已启动")
os.system("git add .")
os.system(cmd)
os.system("git push origin main")
input("请按任意键继续. . . ")