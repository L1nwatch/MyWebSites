# 说明
这个仓库保存的是学习《Python Web TDD：测试驱动开发》时的代码，最终形成的界面如下所示：
![参考界面](https://github.com/L1nwatch/superlists_for_pythonweb/blob/master/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-09-26%2020.26.08.png?raw=true)

# 部署方法
已经编写好了自动部署脚本，下载 `deploy_tools` 文件夹，然后执行命令：
`fab deploy:host=watch@watch0.top:21`，确保 fab 已经安装，用户名和域名以及端口号对应上，即可实现自动部署。

# 相关命令记录
* `python manage.py test lists`，这是运行 lists 的单元测试
* `python manage.py test accounts`，这是运行 accounts 的单元测试
* `python manage.py test functional_tests`，这是运行功能测试
* `python manage.py makemigrations` 迁移，包括这一条：`python manage.py migrate`
* `python manage.py runserver`，跑起服务器

