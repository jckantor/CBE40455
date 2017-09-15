echo "Cleaning up portal"

if "%AGSPORTAL%"=="" (goto NO_ARCGIS_HOME)

set ARCGIS_PYTHON_HOME=%AGSPORTAL%\framework\runtime\python

"%ARCGIS_PYTHON_HOME%\python.exe" cleanup.py

goto END

:NO_ARCGIS_HOME
@echo "Error: AGSPORTAL variable is not set."
@goto END

:END
