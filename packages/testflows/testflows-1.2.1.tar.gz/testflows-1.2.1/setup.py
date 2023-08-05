# Copyright 2019 Vitaliy Zakaznikov (TestFlows Test Framework http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup

setup(
    name="testflows",
    version="1.2.1",
    description="TestFlows Test Framework",
    author="Vitaliy Zakaznikov",
    author_email="vzakaznikov@testflows.com",
    url="https://github.com/testflows/testflows",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    license="Apache-2.0",
    zip_safe=False,
    install_requires=[
        "testflows.core>=1.2.191016.122959",
        "testflows.asserts>=5.2.191016.1221916",
        "testflows.uexpect>=1.2.191016.1222050",
        "testflows.connect>=1.2.191016.1222213"
    ],
    extras_require={
        "dev": [
        ]
    }
)
