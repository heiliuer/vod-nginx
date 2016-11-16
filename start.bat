
@cd refresh_files
@gen.py
@cd ../


@cd www
@start start.bat
@cd ../


@cd "nginx 1.7.11.3 Gryphon"
@start nginx
@nginx -s reload
@cd ../


