# YOLO

*Where interesting souls meet each other!*


## 开发进度

如果执行`pipenv install`命令安装依赖耗时太长，你可以考虑使用国内的PyPI镜像源，比如：
```
$ pipenv install --dev --pypi-mirror https://pypi.tuna.tsinghua.edu.cn/simple
```

复制仓库后，你需要自己创建.flaskenv和.env文件
.flaskenv简单写FLASK_APP="yolo"
FLASK_ENV="development"
.env要写email密码，secret key和数据库连接地址这些敏感信息
