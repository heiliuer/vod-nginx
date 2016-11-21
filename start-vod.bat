@echo off

cd "nginx 1.7.11.3 Gryphon"

echo scanning files
cd vod_server/refresh_files
gen.py>nul
cd ../../

echo reload nginx
tasklist|findstr nginx>nul
if not "%ERRORLEVEL%" == "0" (
	start nginx
) else (
	nginx -s reload
)
cd ../
pause




