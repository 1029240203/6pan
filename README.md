### 6盘多用户文件切换及视频在线播放
#### 注意只对视频文件进行处理
###### 这个只是个人平时写的小玩意bug多不要在意，高手看看就行了不要指点了。
##### 采用flask开发，docker部署。
#### 主要功能：
- 1、添加多用户方便切换
- 2、视频在线播放，原理就是获取到下载地址然后调用在线播放器。限制和下载的时效性一样。
- 3、搜索功能
- 端口为：10003  Vulume:/app
如果没有映射/app目录会自动创建到本地以便于数据持久化
### 除了以上三点再没其它功能了
## 由于6盘还处于开发阶段api随时可能更改，再加上现有已知bug。该应用随时会挂，玩玩就行了。
~~目前不知道哪里原因导致bridge网络模式下无法使用请使用host模式。：本地docker问题造成~~

如需修改端口可修改/etc/nginx/conf.d/nginx.conf和/app/main.py两个文件里的端口信息
