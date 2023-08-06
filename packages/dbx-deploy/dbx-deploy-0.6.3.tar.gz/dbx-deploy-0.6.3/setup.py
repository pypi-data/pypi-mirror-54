# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['DbxDeploy']

package_data = \
{'': ['*'],
 'DbxDeploy': ['Cluster/*',
               'Dbc/*',
               'Git/*',
               'Job/*',
               'Logger/*',
               'Notebook/*',
               'Notebook/Converter/*',
               'Requirements/*',
               'Setup/*',
               'Setup/Version/*',
               'String/*',
               'Whl/*',
               'Workspace/*',
               '_config/*']}

install_requires = \
['PyYAML>=5.1.0,<5.2.0',
 'colorlog>=4.0.0,<4.1.0',
 'databricks-api>=0.3.0,<0.4.0',
 'dbx-notebook-exporter',
 'injecta>=0.4.0,<0.5.0',
 'nbconvert>=5.6.0,<5.7.0',
 'pygit2>=0.28.0,<0.29.0',
 'python-box>=3.4.0,<3.5.0',
 'tomlkit>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['dbx-delete-all-jobs = '
                     'DbxDeploy.JobsDeleterCommand:JobsDeleterCommand.run',
                     'dbx-deploy = '
                     'DbxDeploy.DeployerCommand:DeployerCommand.run',
                     'dbx-deploy-submit-job = '
                     'DbxDeploy.DeployerJobSubmitterCommand:DeployerJobSubmitterCommand.run',
                     'dbx-deploy-with-cleanup = '
                     'DbxDeploy.DeployWithCleanupCommand:DeployWithCleanupCommand.run']}

setup_kwargs = {
    'name': 'dbx-deploy',
    'version': '0.6.3',
    'description': 'Databrics Deployment Tool',
    'long_description': 'Databricks project deployment package\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataSentics/dbx-deploy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.2,<3.6.0',
}


setup(**setup_kwargs)
