import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xyTrader",
    version = "0.0.2",
    author = "xyh",
    author_email ="xiao_yonghui@126.com",
    description = "Quantitative analysis platform",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/xyh888/xyData.git",
    packages = setuptools.find_packages(),
    classifier=[
        "Programming Language :: Python :: 3",
        'Operating System :: Microsoft :: Windows',
    ],
)