@echo off
python build.py code.txt
"C:\Program Files (x86)\UltraISO\UltraISO.exe" -silent -bootfile C:\Users\GIKExe\Desktop\python-compiller\code.txt.bin -file C:\Users\GIKExe\Desktop\python-compiller\code.txt.bin -output C:\Users\GIKExe\Desktop\python-compiller\code.iso
pause