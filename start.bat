
@cd refresh_files
@gen.py>nul
@cd ../

@cd "nginx 1.7.11.3 Gryphon"
@nginx -s reload
@cd ../

@cd www
@create-server.bat
@cd ../
@pause





