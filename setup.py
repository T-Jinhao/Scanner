from setuptools import setup, find_packages

setup(
    name="Scanner",
    version="2.0",
    author="Jinhao",
    author_email="1184028304@qq.com",
    description="基于交互式的自动化信息收集工具",
    # 依赖库
    packages=find_packages(),

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Penetration Test Engineer',

        'Topic :: Software Development :: Information Gathering Tool',

        # 目标 Python 版本
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)