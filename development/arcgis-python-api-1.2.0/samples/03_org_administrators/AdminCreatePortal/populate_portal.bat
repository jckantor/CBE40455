echo "Portal administration scripts"

if "%AGSPORTAL%"=="" (goto NO_ARCGIS_HOME)

set ARCGIS_PYTHON_HOME=%AGSPORTAL%\framework\runtime\python

"%ARCGIS_PYTHON_HOME%\python.exe" create_groups.py
"%ARCGIS_PYTHON_HOME%\python.exe" create_users.py
"%ARCGIS_PYTHON_HOME%\python.exe" publish_content.py

goto END

:NO_ARCGIS_HOME
@echo "Error: AGSPORTAL variable is not set."
@goto END

:END