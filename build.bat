@echo off
chcp 65001 >nul

:: ═══════════════════════════════════════════════════════════════
::  Dovetail Build Script
::    dovetail.exe       - Compiler core
::    dovetail-build.exe - Build tool
:: ═══════════════════════════════════════════════════════════════

:: ── Generate Version ──────────────────────────────────────────
python .\scripts\gen_version.py

:: ── Compiler core ─────────────────────────────────────────────
python -m nuitka --standalone --lto=yes --deployment ^
  --include-module=dovetail.utils.escape_processor ^
  --include-plugin-directory=dovetail/plugins/plugin_api ^
  --include-data-dir=lib=lib ^
  --include-data-dir=proposals=proposals ^
  --output-dir=build ^
  --output-filename=dovetail.exe ^
  main.py

:: ── Build tool ───────────────────────────────────────────────
python -m nuitka --standalone --lto=yes --deployment ^
  --include-module=dovetail.build ^
  --include-module=dovetail.utils.logger ^
  --output-dir=build ^
  --output-filename=dovetail-build.exe ^
  build_main.py

:: ── Copy resources to compiler dist ───────────────────────────
xcopy dovetail\plugins\ build\main.dist\plugins\ /s /y /exclude:build_exclude.txt
xcopy lark\ build\main.dist\lark\ /s /y
xcopy examples\ build\main.dist\examples\ /s /y /exclude:build_exclude.txt
copy NOTICE build\main.dist\NOTICE /y
copy LICENSE build\main.dist\LICENSE /y

:: ── Merge dovetail-build into the same dist ──────────────────
copy build\build_main.dist\dovetail-build.exe build\main.dist\dovetail-build.exe /y