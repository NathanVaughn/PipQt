pyinstaller PipQt.spec
RMDIR /Q /S .\build
xcopy /s .\icons .\dist\PipQt\icons\