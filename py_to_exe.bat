pyinstaller --onefile OOF_Rename.py  --hidden-import ADC_function.py --hidden-import OOF_core.py
rmdir /s/q build
rmdir /s/q __pycache__
pause