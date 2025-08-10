#!/usr/bin/env python3
"""
Setup script for Solsphere System Utility
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Solsphere System Utility - Cross-platform system health monitoring"

setup(
    name="solsphere-utility",
    version="1.0.0",
    description="Cross-platform system health monitoring utility",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Solsphere Team",
    author_email="admin@solsphere.com",
    url="https://github.com/solsphere/system-utility",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "requests>=2.31.0",
        "psutil>=5.9.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "solsphere-utility=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    keywords="system monitoring health security compliance",
    project_urls={
        "Bug Reports": "https://github.com/solsphere/system-utility/issues",
        "Source": "https://github.com/solsphere/system-utility",
        "Documentation": "https://solsphere.com/docs",
    },
)
