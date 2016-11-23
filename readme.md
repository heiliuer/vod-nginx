## windows版 局域网视频服务器(vod)

### 架构

- nginx输出视频流
- python扫描指定目录的视频文件，并生成nginx的配置数据

### 运行环境

- python

### 效果图

![](screenshot/2.png) ![](screenshot/1.png) 


### 如何使用

- 修改 `nginx 1.7.11.3 Gryphon/vod_server/refresh_files/folders.ini` 文件，以回车隔开，例如:

    `d:\Users\Administrator\Pictures`    
    `H:\videos`
    
    > 指定视频文件所在目录
        
- 在项目根目录运行命令

    `start-vod.bat`
    
    > 扫描视频文件，start或者reload nginx
    
- 访问 [http://localhost](http://localhost)
