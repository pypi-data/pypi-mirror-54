# encoding:utf-8
import sys
import os
import shutil
import platform

from setuptools import setup
from Cython.Build import cythonize, build_ext
from Cython.Distutils import Extension as Cython_Extension

arch = platform.architecture()
if arch[0] == "64bit":
    myArch = "64"
elif arch[0] == "32bit":
    myArch = "32"
else:
    raise EnvironmentError("The architecture of platform is error.")

CTP_Version = "v6.3.15"
SRC_NAME = "src"
PRJ_NAME = "CFA"
API_NAME = "CTP"

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "..")
PRJ_DIR = os.path.join(BASE_DIR, SRC_NAME, PRJ_NAME)
API_DIR = os.path.join(PRJ_DIR, API_NAME)
CTP_LIB = os.path.join(API_DIR, "api", CTP_Version)
C2CYTHON_HEADER = os.path.join(API_DIR, "c2cython")
CYTHON2C_HEADER = os.path.join(API_DIR, "cython2c")

TOOLS_PRJ_DIR = os.path.join(CUR_DIR, PRJ_NAME)
if not os.path.exists(TOOLS_PRJ_DIR):
    os.mkdir(TOOLS_PRJ_DIR)
shutil.copy(os.path.join(PRJ_DIR, "__init__.py"), TOOLS_PRJ_DIR)

TOOLS_API_DIR = os.path.join(CUR_DIR, PRJ_NAME, API_NAME)
if not os.path.exists(TOOLS_API_DIR):
    os.mkdir(TOOLS_API_DIR)
shutil.copy(os.path.join(API_DIR, "__init__.py"), TOOLS_API_DIR)
shutil.copy(os.path.join(API_DIR, "ApiStruct.py"), TOOLS_API_DIR)

TOOLS_UTIL_DIR = os.path.join(CUR_DIR, PRJ_NAME, "utils")
if not os.path.exists(TOOLS_UTIL_DIR):
    os.mkdir(TOOLS_UTIL_DIR)
shutil.copy(os.path.join(PRJ_DIR, "utils", "__init__.py"), TOOLS_UTIL_DIR)
shutil.copy(os.path.join(PRJ_DIR, "utils", "base_field.py"), TOOLS_UTIL_DIR)
shutil.copy(os.path.join(PRJ_DIR, "utils", "check_service.py"), TOOLS_UTIL_DIR)
shutil.copy(os.path.join(CUR_DIR, "MyTools.h"), C2CYTHON_HEADER)

package_data = []
extra_link_args = None
extra_compile_args = None

l_myOS = platform.system()
if l_myOS == "Linux":
    CTP_LIB = os.path.join(CTP_LIB, "linux" + myArch)
    package_data.append(CTP_LIB + os.path.sep + "*.so")
    extra_compile_args = ["-Wall"]
    extra_link_args = ['-Wl,-rpath,$ORIGIN']
    l_data_files = [("CFA" + os.path.sep + "CTP", [CTP_LIB + os.path.sep + "libthostmduserapi_se.so"]), ("CFA" + os.path.sep + "CTP", [CTP_LIB + os.path.sep + "libthosttraderapi_se.so"])]
    shutil.copy(os.path.join(CTP_LIB, "libthostmduserapi_se.so"), TOOLS_API_DIR)
    shutil.copy(os.path.join(CTP_LIB, "libthosttraderapi_se.so"), TOOLS_API_DIR)
elif l_myOS == "Windows":
    CTP_LIB = os.path.join(CTP_LIB, "windows" + myArch)
    extra_compile_args = ["/GR", "/EHsc"]
    extra_link_args = []
    package_data.append(CTP_LIB + os.path.sep + "*.dll")
    l_data_files = [("CFA" + os.path.sep + "CTP", [CTP_LIB + os.path.sep + "thostmduserapi_se.dll"]), ("CFA" + os.path.sep + "CTP", [CTP_LIB + os.path.sep + "thosttraderapi_se.dll"])]
    shutil.copy(os.path.join(CTP_LIB, "thostmduserapi_se.dll"), TOOLS_API_DIR)
    shutil.copy(os.path.join(CTP_LIB, "thosttraderapi_se.dll"), TOOLS_API_DIR)
else:
    print("不支持的操作系统")
    sys.exit(1)

common_args = {
    "cython_include_dirs": [CYTHON2C_HEADER, C2CYTHON_HEADER],
    "include_dirs": [CTP_LIB, C2CYTHON_HEADER],
    "library_dirs": [CTP_LIB],
    "language": "c++",
    "extra_compile_args": extra_compile_args,
    "extra_link_args": extra_link_args,
}

l_setup_ext_modules = cythonize([Cython_Extension(name="CFA.CTP.MdApi",
                                                  sources=[os.path.join(BASE_DIR, SRC_NAME, PRJ_NAME, API_NAME, "MdApi.pyx")],
                                                  libraries=["thostmduserapi_se"],
                                                  **common_args),
                                 Cython_Extension(name="CFA.CTP.TraderApi",
                                                  sources=[os.path.join(BASE_DIR, SRC_NAME, PRJ_NAME, API_NAME, "TraderApi.pyx")],
                                                  libraries=["thosttraderapi_se"],
                                                  **common_args)
                                 ],
                                compiler_directives={'language_level': 3, "binding": True}
                                )

setup(
    name=PRJ_NAME,
    version="2.0",
    author='China Futures Assistant',
    author_email='736753634@qq.com',
    license="MIT",
    url="",
    description='China Futures Assistant 中国期货助手',
    long_description='''
China Futures Assistant 中国期货助手 为中国期货交易者提供量化交易功能的软件。

忠实于CTP官方API特性、低延时、易使用是CFA的立身之本。

CFA从以下三个不同的维度实现低延时：

1. 利用Cython技术释放了GIL；

2. 同时支持接入多路行情源，降低轮询等待时间；

3. 利用CTP的线程特性，以接口回调直接驱动策略运行，无需主事件引擎，真正实现去中心化。
我们对CFA进行过严格的延时测试：上海电信300M宽带，Simnow账户以对价方式进行无逻辑报单（收到成交回报之后立即再次报单），平均每秒可以完成50笔成交。也就是说，CFA从发出委托到收到成交回报（这个过程是从本地发出，经过互联网，到达期货公司交易前置，再到交易所，完成撮合成交之后，发回期货公司交易前置，再经过互联网，最终回到客户本地），平均需要20毫秒（1s=1000ms）。
为了提高CFA的易用性，一方面我们力求所有的设计都忠实于CTP官方功能，只要理解CTP官方API的工作流程，就可能直接上手使用，无需学习额外的知识；另一方面，我们会制作系统化的教程，将大家在使用过程中踩坑的几率降到最低。最后，我们开通了www.ctp.plus量化投资研究社区，方便大家学习、分享、交流。
''',
    keywords="CTP Simnow 量化 程序化 算法交易 quant quantitative algotrading",
    platforms=["Windows", "Linux"],
    python_requires=">=3.7",
    include_dirs=[CTP_LIB, CYTHON2C_HEADER],
    packages=["CFA", "CFA.CTP", "CFA.utils"],
    #data_files=l_data_files,
    ext_modules=l_setup_ext_modules,
    cmdclass={'build_ext': build_ext},
    package_data={'': ['*',]},
    zip_safe=False,
)
