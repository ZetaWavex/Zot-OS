import time
import os

t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cmd = f'git commit -m "Update {t}"'

os.system("git add .")
os.system(cmd)
os.system("git push origin main")
input("请按任意键继续. . . ")