@ECHO OFF
SETLOCAL

REM Build from Sphinx Documentation (Windows)
SET SPHINXBUILD=sphinx-build

SET SCRIPT_DIR=%~dp0

SET SOURCEDIR=%SCRIPT_DIR%source
SET BUILDDIR=%SCRIPT_DIR%_build
REM UI docs source directory
SET UISOURCEDIR=%SCRIPT_DIR%..\src\ui\docs\source

IF "%1"=="" GOTO html

"%SPHINXBUILD%" -M %1 "%SOURCEDIR%" "%BUILDDIR%" %SPHINXOPTS% %O%
GOTO end

:html
"%SPHINXBUILD%" -M html "%SOURCEDIR%" "%BUILDDIR%" %SPHINXOPTS% %O%
REM Build UI docs into subfolder 'ui' under html output
"%SPHINXBUILD%" -b html -c "%SOURCEDIR%" "%UISOURCEDIR%" "%BUILDDIR%\html\ui" %SPHINXOPTS% %O%

:end
ENDLOCAL