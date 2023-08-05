#### 一、开始

安装

```shell
pip install glooweb
```

简单使用

```python
from glooweb import Gloo
from wsgiref import simple_server  # 使用wsgiref为我们提供开发服务器

# 实例化一个app对象
app = Gloo()

# 创建一个路由对象,需要传入一个路由前缀参数
api = Gloo.Router("/api")
# 将路由注册进应用
app.register(api)


# 定义视图函数
@api.get("/index")  # 当路径为/api/index, 并且method为get时访问这个视图函数
def index(ctx, request):  # 视图函数需要两个参数，上下文ctx, request请求对象
    return "<h1>index page</h1>"


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 9999
    server = simple_server.make_server(ip, port, app)  # 创建一个wsgi服务
    server.serve_forever()  # 启动服务
```

浏览器中访问127.0.0.1:9999/api/index

![1571132311022](C:\Users\ADMINI~1\AppData\Local\Temp\1571132311022.png)

#### 二、路由

提取URL参数

需求 

url为/product/123456需要将产品ID提取出来

```python
# 定义视图函数
@api.get("/product/{id:int}")  # {id:int}匹配整形字符串
def product(ctx, request):
    print(request.vars.id)  # 访问url中的id的内容
    return f"<h1>product {request.vars.id}</h1>"
```

int匹配整形

word匹配一个单词

str匹配一个字符串

float匹配浮点型

any匹配任意字符

浏览器中访问127.0.01/api/product/123

![1571133119259](C:\Users\ADMINI~1\AppData\Local\Temp\1571133119259.png)

#### 三、拦截器

路由拦截器

```python
# 定义视图函数
@api.get("/product/{id:int}")  # 当路径为/api/index, 并且method为get时访问这个视图函数
def product(ctx, request):  # 视图函数需要两个参数，上下文ctx, request请求对象
    print("视图函数")
    return f"<h1>product {request.vars.id}</h1>"


@api.reg_pre_interceptor
def pre_product(ctx, request):
    print("视图函数响应之前")
    return request


@api.reg_post_interceptor
def post_product(ctx, request, response):
    print("视图函数响应之后")
    return response
```

运行结果

```shell
视图函数响应之前
视图函数
视图函数响应之后
127.0.0.1 - - [15/Oct/2019 18:04:15] "GET /api/product/123 HTTP/1.1" 200 20
```

路由拦截器只对当前路由有效

全局拦截器

```python
# 定义视图函数
@api.get("/product/{id:int}")  # 当路径为/api/index, 并且method为get时访问这个视图函数
def product(ctx, request):  # 视图函数需要两个参数，上下文ctx, request请求对象
    print("视图函数")
    return f"<h1>product {request.vars.id}</h1>"


@api.reg_pre_interceptor
def pre_product(ctx, request):
    print("视图函数响应之前")
    return request


@api.reg_post_interceptor
def post_product(ctx, request, response):
    print("视图函数响应之后")
    return response


@Gloo.reg_pre_interceptor
def pre(ctx, request):
    print("全局响应前视图")
    return request


@Gloo.reg_post_interceptor
def post(ctx, request, response):
    print("全局响应后视图")
    return response
```

运行结果

拦截器及视图函数执行流程

```shell
全局响应前视图
视图函数响应之前
视图函数
视图函数响应之后
全局响应后视图
127.0.0.1 - - [15/Oct/2019 18:55:21] "GET /api/product/123 HTTP/1.1" 200 20
```







