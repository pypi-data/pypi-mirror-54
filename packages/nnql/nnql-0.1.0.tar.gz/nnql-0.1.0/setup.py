# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nnql',
 'nnql.backends',
 'nnql.backends.pytorch',
 'nnql.backends.tensorflow',
 'nnql.tests',
 'nnql.tools']

package_data = \
{'': ['*']}

install_requires = \
['click', 'six', 'typing-extensions']

extras_require = \
{':python_version < "3.7"': ['dataclasses', 'typing', 'contextvars'],
 'all': ['tensorflow==1.14.0', 'torch==1.3.0', 'torchvision==0.4.1'],
 'pytorch': ['torch==1.3.0', 'torchvision==0.4.1'],
 'tensorflow': ['tensorflow==1.14.0']}

entry_points = \
{'console_scripts': ['nnql = nnql.cli:nnql']}

setup_kwargs = {
    'name': 'nnql',
    'version': '0.1.0',
    'description': 'graph instrumentation',
    'long_description': '## Create a virtual environment\n\n```bash\nconda env create -f environment.yml\nsource activate nnql\n```\n\n## Install dependencies\n\nThere are two options:\n\n- Use pip:\n    ```bash\n    pip install -e ".[all]"\n    ```\n- Use poetry:\n    ```bash\n    poetry install -E all\n    ```\n\n## Install git pre-commit hooks\n\n```bash\npre-commit install\n```\n',
    'author': 'uchuhimo',
    'author_email': 'uchuhimo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uchuhimo/nnql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
