from setuptools import setup

setup(
    name="bot",
    version="0.1",
    py_modules=["bot-cli"],
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
