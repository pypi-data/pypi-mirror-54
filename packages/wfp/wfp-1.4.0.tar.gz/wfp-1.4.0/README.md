# 1、开发环境准备
使用Pycharm IDE进行wf-pipeline-service的开发，并使用python virtualenv来开发调试该工程。virtualenv使用3.6及以上的python开发环境。

# 2、工程目录说明

- src，该目录为Pipeline服务的源代码目录，Pipeline服务的入口程序为bootstrap.py。


# 3、如何运行启动Pipeline服务

## 3.1、安装系统依赖的package
```
pip install -r requirements.txt
```

## 3.2、如何在本地启动Pipeline服务
```
python src/bootstrap.py
```