@cd "nginx 1.7.11.3 Gryphon"

@cd vod_server/refresh_files
@gen.py>nul
@cd ../../

@cd ../
@nginx -s reload





