Remove-Item .\dist -Force -Recurse -ErrorAction Ignore
pyinstaller PipQt.spec
Remove-Item .\build -Force -Recurse
Copy-Item .\icons .\dist\PipQt\icons -Force -Recurse