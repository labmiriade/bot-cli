from setuptools import setup, find_packages

setup(
    name="bot",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==7.1.2",
        "requests==2.25.1",
        "toml==0.10.2",
        "fcache==0.4.7",
    ],
    entry_points="""
        [console_scripts]
        bot=src.main:cli
    """,
)
