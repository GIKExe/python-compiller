@echo off
python build.py %cd%\code.txt -boot
uiso-pp.exe -silent -bootfile %cd%\out\code.bin -file %cd%\out\code.bin -output %cd%\out\code.iso
pause