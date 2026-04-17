---
title: 'FastAPI'
description: 'FastAPI最佳实践，一个用于构建API的现代、快速web框架'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - Web开发
  - Python
  - FastAPI
---

## 摘要
FastAPI 最佳实践

## 正文
🚀`fastapi`，一个用于构建 API 的现代、快速（高性能）的web框架。

`fastapi`是建立在Starlette和Pydantic基础上的，Pydantic是一个基于Python类型提示来定义数据验证、序列化和文档的库。Starlette是一种轻量级的ASGI框架/工具包，是构建高性能Asyncio服务的理性选择。

> [!TIP] FastAPI 的优势

⚡ 快速：可与 NodeJS 和 Go 比肩的极高性能（归功于 Starlette 和 Pydantic），是最快的 Python web 框架之一。
🚀 高效编码：提高功能开发速度约 200％ 至 300％。
🐛 更少bug：减少约 40％ 的人为（开发者）导致错误。
🧠 智能：极佳的编辑器支持。处处皆可自动补全，减少调试时间。
📝 简单：设计的易于使用和学习，阅读文档的时间更短。
📦 简短：使代码重复最小化。通过不同的参数声明实现丰富功能。
🛡️ 健壮：生产可用级别的代码。还有自动生成的交互式文档。

Python 版本要求: Python3.8 +

## 技术栈

FastAPI 站在以下巨人的肩膀之上：

### Starlette 负责 web 部分

* 源码地址：https://github.com/encode/starlette

* 文档地址：https://www.starlette.io/

### Pydantic 负责数据部分

* 源码地址：https://github.com/pydantic/pydantic

* 文档地址：https://docs.pydantic.dev/latest/

> [!NOTE]
本文以一个RBAC权限管理系统为例说明 FastAPI 的使用

## 快速开始 🚀

```bash
pip install fastapi
```

你还会需要一个 ASGI 服务器，生产环境可以使用Uvicorn

```bash
pip install uvicorn
```

```python
from fastapi import FastAPI  # FastAPI 是一个为你的 API 提供了所有功能的 Python 类。

app = FastAPI()  # 这个实例将是创建你所有 API 的主要交互对象。这个 app 同样在如下命令中被 uvicorn 所引用

@app.get("/")
async def root():
    return {"message": "Hello shouyu"}
```

通过以下命令运行服务器：

```bash
uvicorn main:app --reload
```

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [73408]
INFO:     Started server process [73408]
INFO:     Waiting for application startup
INFO:     Application startup complete
```

也可以直接运行：

```python
if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, debug=True, reload=True)
```

> [!TIP] 创建 FastAPI 应用的步骤
（1）导入 FastAPI。
（2）创建一个 app 实例。
（3）编写一个路径操作装饰器（如 @app.get("/")）。
（4）编写一个路径操作函数（如上面的 def root(): ...）
（5）定义返回值
（6）运行开发服务器（如 uvicorn main:app --reload）

此外，fastapi有着**非常棒的交互式 API 文档**，这一点很吸引人。

跳转到http://127.0.0.1:8080/docs你将会看到**自动生成**的交互式 API 文档。

## 路径参数 🔗

以使用与 Python 格式化字符串相同的语法来声明路径"参数"或"变量"：

```python
@app.get("/user/{user_id}")
def get_user(user_id: int):
    print(user_id, type(user_id))
    return {"user_id": user_id}
```

路径参数`user_id`的值将作为参数`user_id`传递给你的函数。并且引入类型注解，规定了传进来的参数类型。这在以后会经常见到。

### 基本使用

路径函数中声明不属于路径参数的其他函数参数时，它们将被自动解释为"查询字符串"参数，就是 url? 之后用`&`分割的 key-value 键值对。

```python
@app.get("/jobs/{kd}")
async def search_jobs(kd: str, city: str|None = None, xl: str|None = None):  # 有默认值即可选，否则必选
    if city or xl:
        return {"kd": kd, "city": city, "xl": xl}
    return {"kd": kd}
```

### 枚举

当你想限定传入的参数的类型只能是规定好的几个，那么你可以使用枚举

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    
    # 2 获取枚举类型的值
    # 使用 model_name.value 或 your_enum_member.value 获取实际的值
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    # 3 返回枚举类型，直接返回对象即可
    print(type(model_name))
    return {"model_name": model_name, "message": "Have some residuals"}
```

### 路径转换器

FastAPI 支持路径转换器，可以接收包含路径的参数，即参数中可以含有`/`。使用`path`类型来接收完整的路径，包括正斜杠（/）：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    :path 转换器允许参数包含路径分隔符
    示例访问: /files/home/user/test.txt
    """
    return {"file_path": file_path}
```

### 路径参数使用 Path 校验

Path 类提供了丰富的参数校验功能，可以对路径参数进行详细的限制和验证：

```python
from fastapi import FastAPI, Path, HTTPException
from typing import Literal
from enum import Enum

app = FastAPI()

class UserType(str, Enum):
    ADMIN = "admin"
    NORMAL = "normal"
    VIP = "vip"

@app.get("/users/{user_id}/profile/{user_type}")
async def get_user_profile(
    # 用户ID：必须是正整数且在100-999999之间
    user_id: int = Path(
        ...,  # ... 表示必填参数
        gt=100, 
        lt=1000000,
        title="用户ID",
        description="用户的唯一标识符",
        example=12345
    ),
    # 用户类型：必须是预定义的枚举值之一
    user_type: UserType = Path(
        ...,
        title="用户类型",
        description="用户的角色类型"
    ),
):
    if user_id == 404:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    return {
        "user_id": user_id,
        "user_type": user_type,
        "message": f"获取 {user_type.value} 类型用户 {user_id} 的详细信息"
    }

@app.get("/files/{year}/{month}/{day}/{filename}")
async def get_file(
    # 年份：必须是2000-2030之间的整数
    year: int = Path(..., ge=2000, le=2030),
    # 月份：必须是1-12之间的整数
    month: int = Path(..., ge=1, le=12),
    # 日期：必须是1-31之间的整数
    day: int = Path(..., ge=1, le=31),
    # 文件名：必须符合特定格式
    filename: str = Path(
        ...,
        min_length=1,
        max_length=100,
        regex="^[a-zA-Z0-9_-]+\.(jpg|png|pdf)$",
        title="文件名",
        description="支持jpg、png和pdf格式的文件"
    ),
):
    return {
        "file_path": f"{year}/{month}/{day}/{filename}",
        "message": "文件信息获取成功"
    }
```

> [!TIP] Path校验器的常用参数

... 或 None: 表示参数是否必填
gt/lt/ge/le: 数值大小限制(大于/小于/大于等于/小于等于)
min_length/max_length: 字符串长度限制
regex: 正则表达式验证
title/description: 参数说明(会在API文档中显示)
example: 示例值
deprecated: 标记参数即将废弃

示例请求:

/users/12345/profile/admin
/files/2024/4/9/document-2024.pdf

## 查询参数 🔍

### 基本使用

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为**查询**参数

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### 查询参数类型强制转换

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

> [!NOTE]
本例中，访问：
http://127.0.0.1:8000/items/foo?short=1
或
http://127.0.0.1:8000/items/foo?short=True
或
http://127.0.0.1:8000/items/foo?short=true
或
http://127.0.0.1:8000/items/foo?short=on
或
http://127.0.0.1:8000/items/foo?short=yes
或其它任意大小写形式（大写、首字母大写等），函数接收的 short 参数都是布尔值 True。值为 False 时也一样

### 必选查询参数

如果没有设置默认值，则必填

```python
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    #1 没设置默认值，参数必须填
    item = {"item_id": item_id, "needy": needy}
    return item

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    # 2 skip 和limit可以不填
    '''
    needy，必选的 str 类型参数
    skip，默认值为 0 的 int 类型参数,可以不填
    limit，可选的 int 类型参数
    '''
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

### 查询参数使用Query校验

Query 类提供了丰富的参数校验功能，可以对查询参数进行详细的限制和验证：

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/items/")
async def read_items(
    # 必填，长度3-50个字符
    name: str = Query(..., min_length=3, max_length=50),
    
    # 可选，设置默认值，只能是正数
    age: int = Query(default=18, gt=0, lt=120),
    
    # 正则表达式验证
    mobile: str = Query(None, regex="^1[3-9]\d{9}$"),
    
    # 多个允许值
    category: str = Query(None, enum=["A", "B", "C"]),
    
    # 接收多个相同参数
    tags: List[str] = Query(
        default=[],
        title="标签列表",
        description="用于筛选的标签",
        min_items=1,     # 至少一个标签
        max_items=5      # 最多5个标签
    ),
    
    # 添加示例值和描述
    q: str = Query(
        None,
        title="搜索字符串",
        description="要搜索的关键词",
        example="上海陆家嘴"
    ),
):
    results = {
        "name": name,
        "age": age,
        "mobile": mobile,
        "category": category,
        "tags": tags,
        "q": q
    }
    return results
```

> [!TIP] 示例请求
/items/?name=张三&age=25&mobile=13812345678&category=A&tags=tag1&tags=tag2&q=test
Query 的常用参数:

...: 该参数必填
default: 默认值
min_length/max_length: 字符串长度限制
gt/lt/ge/le: 数值大小限制(大于/小于/大于等于/小于等于)
regex: 正则表达式验证
enum: 枚举允许值
title/description: OpenAPI文档说明
example: 示例值
min_items/max_items: 列表元素数量限制

## 请求体(必须以json格式) 📦

当你需要将数据从客户端（例如浏览器）发送给 API 时，你将其作为「请求体」发送。**请求**体是客户端发送给 API 的数据。**响应**体是 API 发送给客户端的数据。

FastAPI 基于`Pydantic`，`Pydantic`主要用来做类型强制检查（校验数据）。不符合类型要求就会抛出异常。

对于 API 服务，支持类型检查非常有用，会让服务更加健壮，也会加快开发速度，因为开发者再也不用自己写一行一行的做类型检查。

```bash
pip install pydantic
```

### 基本使用

```python
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
import aiomysql
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    # 写字段
    name: str  # name 是字符串类型，必传
    price: int = Field(default=66, gt=30) # price 可以不传，必须大于30
    description: str | None = None  # description是str类型或其他类型，可以不传


@app.post("/items")
async def read_items(item: Item):
    print(item)  # Item的对象
    print(item.dict())  # 转成字典
    return {"data": "read_items"}
```

### 表单数据

在 OAuth2 规范的一种使用方式（密码流）中，需要将用户名、密码作为表单字段发送，而不是 JSON。

FastAPI 可以使用**Form**组件来接收表单数据，需要先使用`pip install python-multipart`命令进行安装。

```python
from fastapi import FastAPI,Form
from pydantic import BaseModel, Field
from typing import List
app = FastAPI()

@app.post("/regin")
def regin(username: str = Form(..., max_length=16, min_length=8, regex='[a-zA-Z]'),
          password: str = Form(..., max_length=16, min_length=8, regex='[0-9]')):
    print(f"username:{username},password:{password}")
    return {"username": username}
```

对于表单提交，FastAPI 还提供了另一种方式。

```python
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request

app = FastAPI()

@app.post("/regin")
async def read_info(request: Request):
    form = await request.form()
    return {"name": form.get("username"),
            "password": form.get("password")}
```

### 请求体嵌套

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str | None = None
    price: int = Field(gt=10) # 这里的 Field 的用法同 Query 和 Path
    tags: List[str] = []
    images: List[Image] = None


@app.post('/item/')
async def index(item: Item):
    print(item.dict())
    return '请求体'
```

### 请求体示例

一个简单的用户管理API示例，展示请求体的序列化和反序列化：

```python
# filepath: models.py
from tortoise import fields, models
from passlib.hash import bcrypt

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100)
    password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    department = fields.ForeignKeyField('models.Department', related_name='users', null=True)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

class Department(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
```

```python
# filepath: user.py
from fastapi import APIRouter
from ..models import UserInfo
from ..schemas import UserSchema
router = APIRouter()

@app.get('/users/{user_id}', description="查询单个用户")
async def get_user_info(
        user_id: int,
):
    # 根据用户id，拿到用户
    user = await UserInfo.filter(id=user_id).prefetch_related("roles", 'dept', 'jobs').first()
    # 使用pydantic 序列化
    if user:
        user_dict = await UserSchema.from_common_orm(user)
        return APIResponse(result=user_dict)
        # 返回给前端
    else:
        raise Exception('该用户不存在')

@router.post('/users', description="新增用户接口")
async def create_user(
        user_in: UserInSchema,
        # user: UserInfo = Depends(get_current_user)
):
    roles = user_in.roles or []
    jobs = user_in.job or []
    del user_in.roles
    del user_in.job
    password = UserInfo.make_password('123456')
    user_new = await UserInfo.create(**user_in.dict(), password=password)
    for role_id in roles:
        role = await Roles.get(id=role_id)
        await user_new.roles.add(role)
    for job_id in jobs:
        job = await Job.get(id=job_id)
        await user_new.job.add(job)
    return APIResponse(msg='创建成功')
```

```python
# filepath: schemas.py
class UserInSchema(BaseModel):
    username: str
    nick_name: str
    gender: int
    email: str
    phone: int
    is_active: bool
    roles: List[int] | None = []
    dept_id: int | None = None
    job: List[int] | None = []

class UserSchema(BaseModel):
    id: int
    username: str
    nick_name: str
    gender: int
    avatar: str  # 都带一个固定前缀
    email: str
    phone: str
    is_active: bool
    roles_detail: Any | None = []

    roles: Any | None = []
    dept_id: int | None = []
    job: Any | None = []

    # dept:DeptSchema|None=None
    # job:List[JobSchema]|None=[]

    # 使用pydantic 把对象转成字典，要带它
    class Config:
        from_attributes = True

    @classmethod
    async def from_common_orm(cls, obj):
        obj_dict = cls.from_orm(obj).dict()
        obj_dict['avatar'] = f"http://{setting.APP_HOST}:{setting.APP_PORT}/media/{obj_dict['avatar']}"  # 在某个字段前后加固定的
        roles = await obj.roles.all()
        obj_dict['roles_detail'] = [{'id': role.id, 'name': role.name} for role in roles]
        obj_dict['roles'] = [role.id for role in roles]
        obj_dict['dept_id'] = obj.dept_id
        obj_dict['job'] = [job.id for job in await obj.job.all()]
        return obj_dict
```

```python
# filepath: schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    department_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    department: Optional[dict] = None

    class Config:
        from_attributes = True

    @classmethod
    async def from_orm_custom(cls, user):
        user_dict = cls.from_orm(user).dict()
        if user.department:
            user_dict['department'] = {
                'id': user.department.id,
                'name': user.department.name
            }
        return user_dict
```

```python
# filepath: routes.py
from fastapi import APIRouter, HTTPException, Path
from typing import List
from .models import User, Department
from .schemas import UserCreate, UserResponse

router = APIRouter()

@router.post("/users/", response_model=UserResponse, tags=["users"])
async def create_user(user_in: UserCreate):
    """创建新用户"""
    # 检查用户名是否已存在
    if await User.filter(username=user_in.username).exists():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建用户实例
    user_dict = user_in.dict()
    department_id = user_dict.pop('department_id', None)
    
    # 哈希密码
    user_dict['password'] = User.hash_password(user_dict['password'])
    
    # 创建用户
    user = await User.create(**user_dict)
    
    # 关联部门
    if department_id:
        department = await Department.get_or_none(id=department_id)
        if department:
            user.department = department
            await user.save()
    
    return await UserResponse.from_orm_custom(user)

@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(
    user_id: int = Path(..., gt=0, description="用户ID")
):
    """获取用户详情"""
    user = await User.get_or_none(id=user_id).prefetch_related('department')
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return await UserResponse.from_orm_custom(user)
```

```python
# filepath: main.py
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .routes import router

app = FastAPI(title="用户管理API")

# 注册路由
app.include_router(router, prefix="/api/v1")

# 注册数据库
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
```

## Request对象 🔄

```python
from fastapi import FastAPI,Request

app = FastAPI()

@app.post('/')
async def index(request:Request): # 等同于django的request对象--》只是有些名字不一样
    print(request.method) # 请求方式
    data=await request.json()#把请求体转成json格式--》编码格式需要是jsong
    print(data)
    print(request.url) #请求地址
    print(request.client.host) # 客户端ip
    print(request.client.port) # 客户端端口
    print(request.headers) # 请求头--》 user-agent在里面
    print(request.cookies) # cookie
    return 'ok'
```

## 静态资源 📁

在 Web 开发中，需要请求很多静态资源文件（不是由服务器生成的文件），如 css/js 和图片文件等。

```bash
pip install aiofiles
```

```python
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"))
```

## 响应模型 📊

### 路径操作的response_model

#### （1）response_model

前面写的这么多路径函数最终 return 的都是自定义结构的字典，FastAPI 提供了 response_model 参数，声明 return 响应体的模型

```python
# 路径操作
@app.post("/items/", response_model=Item)
# 路径函数
async def create_item(item: Item):
    ...
```

> [!IMPORTANT]
response_model 是路径操作的参数，并不是路径函数的参数哦

FastAPI将使用`response_model`进行以下操作：

* 将输出数据转换为response_model中声明的数据类型。

* 验证数据结构和类型

* 将输出数据限制为该model定义的

* 添加到OpenAPI中

* 在自动文档系统中使用。

你可以在任意的路径操作中使用`response_model`参数来声明用于响应的模型

案例：

* 注册功能

* 输入账号、密码、昵称、邮箱，注册成功后返回个人信息

```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

#### （2）response_model_exclude_unset

通过上面的例子，我们学到了如何用response_model控制响应体结构，但是如果它们实际上没有存储，则可能要从结果中忽略它们。例如，如果model在NoSQL数据库中具有很多可选属性，但是不想发送很长的JSON响应，其中包含默认值。

案例：

```python
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

请求：http://127.0.0.1:8080/items/foo

不设置unset参数：

```json
{
  "name": "Foo",
  "description": null,
  "price": 50.2,
  "tax": 10.5,
  "tags": []
}
```

设置unset参数：

```json
{
  "name": "Foo",
  "price": 50.2
}
```

使用路径操作装饰器的`response_model`参数来定义响应模型，特别是确保私有数据被过滤掉。使用`response_model_exclude_unset`来仅返回显式设定的值。
除了`response_model_exclude_unset`以外，还有`response_model_exclude_defaults`和`response_model_exclude_none`，我们可以很直观的了解到他们的意思，不返回是默认值的字段和不返回是None的字段。

#### （3）INCLUDE和EXCLUDE

```python
# response_model_exclude
@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"description"}, )
async def read_item(item_id: str):
    return items[item_id]

# response_model_include  
@app.get("/items/{item_id}", response_model=Item, response_model_include={"name", "price"}, )
async def read_item(item_id: str):
    return items[item_id]
```

### 路径函数的response_model

除了使用 路径操作的`response_model`参数限制返回值，还可以在路径函数的返回值加上类型声明。

```python
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
import aiomysql
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):  # 这个类必须继承pydantic的BaseModel
    # 写字段
    name: str  # name 是字符串类型，必传
    price: int = 99  # price是int类型，可以不传
    description: str | None = None # description是str类型或其他类型，可以不传
class ItemOut(BaseModel):
    name: str
    description: str

@app.post("/items")
# async def read_items(item:Item): # 返回的类型是Item
async def read_items(item:Item)->ItemOut: # 返回的类型是ItemOut，没有price
    return item # 对象可以直接返回
```

## cookie使用 🍪

```python
from fastapi import FastAPI,Request,Cookie

app = FastAPI()

@app.post('/')
async def index(name:str=Cookie()):
    print(name)
    return 'ok'
```

## 文件上传 📤

```python
# 小文件上传--》一次性取到内存，保存到文件中
# 大文件上传--》一点点取到内存保存到文件中

from fastapi import FastAPI,Form,File,UploadFile
from pydantic import BaseModel, Field
from typing import List
app = FastAPI()

# 小文件上传
@app.post('/file/')
async def little_file(file:bytes=File()):
    # file 就是文件二进制内容
    with open('a.txt','wb') as f:
        f.write(file)
    return {'file_size':len(file)}
# 大文件上传
@app.post('/uploadfile/')
async def big_file(file:UploadFile):
    # file是文件对象
    print(file)
    # 打开文件，一点点取出来写进入
    with open(file.filename, "wb") as buffer:
        while True:
            data = await file.read(1024)
            if not data:
                break
            buffer.write(data)

    return {'file_size':file.filename}
```