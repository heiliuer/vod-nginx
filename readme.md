#### vod-nginx nginx流媒体服务器

> [参考文档](https://my.oschina.net/gaga/blog/478480)


1. 启动nginx

`start nginx`

2. 推送rtmp流到nginx-rtmp

`start ffmpeg -re -i rtmp://live.hkstv.hk.lxdns.com/live/hks -vcodec libx264 -preset:v ultrafast -tune:v zerolatency -acodec copy -f flv rtmp://localhost:1935/hls/mystream -loglevel quiet`

3. rtmp直播

`start ffplay "rtmp://127.0.0.1:1935/hls/mystream"`

4. hls 直播

`start ffplay "http://127.0.0.1:18080/hls/mystream.m3u8"`

5. 开始录制

`start http://127.0.0.1:18080/control/record/start?app=hls&name=mystream&rec=rec`

6. 停止录制

`start http://127.0.0.1:18080/control/record/stop?app=hls&name=mystream&rec=rec`

7. 为rtmp点播文件添加索引，否则文件在播放时进度条不能拖动，假定刚才录制的文件名为mystream-1428384476_rec.flv

`start yamdi -i nginx-rtmp-module\tmp\rec\mystream-1428384476_rec.flv -o nginx-rtmp-module\tmp\rec\mystream-1428384476_rec_idx.flv`

8. rtmp点播

`start ffplay "rtmp://127.0.0.1:1935/vod2/mystream-1428384476_rec_idx.flv"`

9. 制作hls点播分片文件

`start ffmpeg -i nginx-rtmp-module\tmp\rec\mystream-1428384476_rec.flv -acodec copy -bsf:a h264_mp4toannexb -g 105 -vcodec libx264 -vprofile baseline -bf 0 -bufsize 850k -bsf:v dump_extra -map 0 -f segment -segment_format mpegts -segment_list "nginx-rtmp-module\tmp\rec\mystream-1428384476_rec\mystream-1428384476_rec.m3u8" -segment_time 10 nginx-rtmp-module\tmp\rec\mystream-1428384476_rec\mystream-1428384476_rec-%d.ts`

10. hls 点播

`start ffplay "http://127.0.0.1:8080/vod/mystream-1428384476_rec/mystream-1428384476_rec.m3u8"`