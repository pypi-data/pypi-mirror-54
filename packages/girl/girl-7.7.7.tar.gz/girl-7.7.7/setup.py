'''
@File       :   setup.py
@Author     :   Jiang Fubang
@Time       :   2019-10-28 17:22
@Version    :   1.0
@Contact    :   luckybang@163.com
@Dect       :   None
'''

from setuptools import setup, find_packages     # 这个包没有可以pip一下

setup(
    name = "girl",      # 这个是pip项目发布的名称
    version = "7.7.7",      # 版本号，pip默认安装最新版
    keywords = ("pip", "女孩","girl"),
    description = "蒋付帮utils",
    long_description = "",
    license = "MIT Licence",

    url = "https://github.com/jiangfubang",       # 项目相关文件地址，一般是github，有没有都行吧
    author = "Jiang Fubang",
    author_email = "luckybang@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any"
)