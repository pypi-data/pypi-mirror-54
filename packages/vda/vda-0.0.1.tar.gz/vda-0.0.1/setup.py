#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.command.build import build
from distutils.command.clean import clean
from setuptools.command.test import test
import os
import shutil

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst")) as f:
    long_description = f.read()


class Clean(clean):

    normal_list = [
        "dist",
        "vda.egg-info",
        "vda/grpc/agent_pb2_grpc.py",
        "vda/grpc/agent_pb2.py",
    ]

    force_list = [
        ".eggs",
        ".coverage",
    ]

    def run(self):
        super(Clean, self).run()
        self._clean_file_or_dir(self.normal_list)
        for dir_name in ["vda", "tests"]:
            dir_path = os.path.join(here, dir_name)
            self._clean_cache(dir_path)
        if self.all:
            self._clean_file_or_dir(self.force_list)

    def _clean_file_or_dir(self, inp_list):
        for inp in inp_list:
            full_path = os.path.join(here, inp)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            elif os.path.isfile(full_path):
                os.remove(full_path)

    def _clean_cache(self, root_name):
        for dir_name, subdir_list, file_list in os.walk(root_name):
            if dir_name.endswith("/__pycache__"):
                shutil.rmtree(dir_name)


def grpc_compile():
    from grpc_tools import protoc
    protoc.main((
        "",
        "--proto_path=.",
        "--python_out=.",
        "--grpc_python_out=.",
        "vda/grpc/agent.proto",
    ))


class Build(build):

    def run(self):
        grpc_compile()
        super(Build, self).run()


class Test(test):

    def run(self):
        import coverage
        grpc_compile()
        cov = coverage.Coverage()
        cov.start()
        super(Test, self).run()
        cov.stop()
        cov.save()
        cov.report(show_missing=True, include="vda/*", omit="*pb2*")


setup(
    name="vda",
    version="0.0.1",
    description="virtual disk array",
    long_description=long_description,
    url="https://github.com/yupeng0921/vda",
    author="peng yu",
    author_email="yupeng0921@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords="storage",
    python_requires=">=3.6",
    setup_requires=[
        "flake8",
        "coverage",
        "grpcio-tools",
    ],
    install_requires=[
        "marshmallow",
        "SQLAlchemy",
        "grpcio",
        "protobuf",
    ],
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "vda": [
            "common/default.cfg",
        ],
    },
    entry_points={
        "console_scripts": [
            "vda_monitor=vda.monitor.launcher:launch_monitor",
            "vda_data_node=vda.agent.data_node:launch_data_node",
        ]
    },
    cmdclass={
        "clean": Clean,
        "build": Build,
        "test": Test,
    },
)
