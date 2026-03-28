python -m nuitka --standalone --lto=yes --deployment --include-module=dovetail.utils.escape_processor --include-plugin-directory=dovetail/plugins/plugin_api --include-data-dir=lib=lib --include-data-dir=docs=docs --include-data-dir=proposals=proposals --include-data-dir=example=example --output-dir=build --output-filename=dovetail.exe  .\main.py
xcopy dovetail\plugins\ build\main.dist\plugins\ /s /y
xcopy lark\ build\main.dist\lark\ /s /y
xcopy NOTICE build\main.dist\ /y
xcopy LICENSE build\main.dist\ /y
