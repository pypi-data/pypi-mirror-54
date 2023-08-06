from setuptools import setup, find_packages

parse_requirements = ['SQLAlchemy', 'PyMySQL']

setup(
    name="mageia",
    version="0.1.1",
    description="DataBase engine for you",
    long_description="Pascal by stefanlei",
    license="Apache",
    url="https://mageia.cn",
    author="stefanlei",
    author_email="stefanlei@qq.com",
    # 需要构建哪些包，一般来说就这样即可，或者手动指定。
    packages=find_packages(),
    # 需要安装的依赖包
    install_requires=parse_requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
