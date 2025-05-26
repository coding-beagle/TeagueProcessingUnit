from setuptools import setup

setup(
    name="TeagueASM",
    version="0.1.0",
    description="Helper tool to convert .hex files to TeagueASM, and vice versa.",
    author="coding-beagle",
    author_email="nicholasp.teague@gmail.com",
    packages=["TeagueASM"],
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        tgasm=TeagueASM.main:cli
    """,
)
