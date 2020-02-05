pyinstaller -y -F -i ./np.ico "main.py"

move dist/main.exe ../

rmdir /s /q build __pycache__ 

del /s /q main.spec

cd dist

move main.exe ../kor-np.exe

cd ..

rmdir /s /q dist

exit