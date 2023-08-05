#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup
import os

package_name = "dbt-snowflake"
package_version = "0.15.0b1"
description = """The snowflake adapter plugin for dbt (data build tool)"""

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    author="Fishtown Analytics",
    author_email="info@fishtownanalytics.com",
    url="https://github.com/fishtown-analytics/dbt",
    packages=find_packages(),
    package_data={
        'dbt': [
            'include/snowflake/dbt_project.yml',
            'include/snowflake/macros/*.sql',
            'include/snowflake/macros/**/*.sql',
        ]
    },
    install_requires=[
        'dbt-core=={}'.format(package_version),
        'snowflake-connector-python>=1.6.12,<2.1',
    ]
)
