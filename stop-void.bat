@cd "nginx 1.7.11.3 Gryphon"

@echo stopping
@tasklist|findstr nginx>nul
@if "%ERRORLEVEL%"=="0" @nginx -s stop






