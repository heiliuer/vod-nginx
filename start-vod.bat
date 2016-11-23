@echo off

cd "nginx 1.7.11.3 Gryphon"

echo scanning files
cd vod_server/refresh_files
gen.py>nul
cd ../../


tasklist|findstr nginx>nul
if not "%ERRORLEVEL%" == "0" (
    echo start nginx
	start nginx
) else (
    echo reload nginx
	nginx -s reload
)

::start vod_server/refresh_files/ipStart.py 80

cd ../

echo exit ... 2s 
ping 127.1 -n 2 >nul




