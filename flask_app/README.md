# flask_my_blog

### 项目目录结构

```c#
📦 flask_project
├─ api // 资源定位
│  ├─ resources // API模块
│  │  └─ target_resources.py
│  ├─ schemas // 序列化、数据校验
│  │  └─ targ et_schema.py
│  └─ views.py
├─ auth // 用户鉴权验证
│  ├─ decorators.py
│  ├─ helpers.py
│  └─ views.py
├─ doc
├─ env // 环境变量（仅存储于项目本地，不上传至云端）
│  ├─ .env
│  └─ .env.db_connection
├─ instance  // PyCharm生成的数据库实例
├─ migrations // 数据迁移
models  // ORM(对象关系映射 Object-Relational Mapping)
│  └─ target_do.py
├─ packages // 第三方依赖管理
│  └─ database_connecter.py
├─ seed // 种子数据库数据
   ├─ roles.sql
   └─ target.sql
├─ static
├─ uploads // 上存的资源存储位置
├─ app.py // 项目的启动入口文件
├─ config.py // 项目的配置项文件
├─ constants.py // 缓存的时间设置
├─ Dockerfile
├─ manage.py // 自定义flask的shell脚本命令
├─ poetry.lock
├─ pyproject.toml // poetry的配置项文件
├─ seed.py //种子数据库执行脚本
└─ targets.py
```


### 对象关系映射（Object-Relational Mapping，ORM）

ORM 是一种编程技术，用于将对象模型与关系数据库之间进行映射，从而允许开发者在编写应用程序时使用面向对象的方式来操作数据库，而不需要直接编写 SQL 查询语句。