from setuptools import setup, find_packages

setup(
    name="ns-packages",
    version="0.1.0",
    description="NASA数据聚合系统共享包",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.11",
)
