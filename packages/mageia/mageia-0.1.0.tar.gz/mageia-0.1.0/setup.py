from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="mageia",
    version="0.1.0",
    description="DataBase engine for you",
    long_description="Pascal by stefanlei",
    license="Apache",
    url="https://mageia.cn",
    author="stefanlei",
    author_email="stefanlei@qq.com",
    # 需要构建哪些包，一般来说就这样即可，或者手动指定。
    packages=find_packages(),
    # 需要安装的依赖包
    install_requires=parse_requirements("requirements.txt"),
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
