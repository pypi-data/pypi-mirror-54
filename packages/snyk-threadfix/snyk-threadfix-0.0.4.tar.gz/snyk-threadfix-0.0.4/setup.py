# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snyk_threadfix']

package_data = \
{'': ['*']}

install_requires = \
['arrow', 'poetry-version>=0.1.5,<0.2.0', 'pysnyk>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['snyk-threadfix = snyk_threadfix.main:run']}

setup_kwargs = {
    'name': 'snyk-threadfix',
    'version': '0.0.4',
    'description': '',
    'long_description': "# snyk-threadfix\n\nThe ThreadFix / Snyk integration allows you to view open source vulnerabilities identified by Snyk on the ThreadFix platform and direct you to comprehensive information and remediation guidance.\n\n`snyk-threadfix` allows you to generate a `.threadfix` file from Snyk project data. It outputs JSON data in the ThreadFix file format - printing to standard out or a specified filename. It does not upload directly to ThreadFix at present but there is a ThreadFix API endpoint that you can use: [ThreadFix Upload Scan API](https://denimgroup.atlassian.net/wiki/spaces/TDOC/pages/22908335/Upload+Scan+-+API).\n\n## Installation\n```\npip install snyk-threadfix\n```\n\n## Configuration\nYou must first obtain a Snyk API token from your [Snyk account](https://app.snyk.io/login). Once you have a token you must either install the [Snyk CLI](https://github.com/snyk/snyk) and run `snyk auth <your-token>` or simply run:\n```\nexport SNYK_TOKEN=<your-token> \n```\n\n## Usage\nYou must first identify your Snyk org ID. This is easy - simply log into your Snyk account, click on Settings, and find your Organization ID there. If you have multiple orgs in your Snyk account, make sure to first choose the one you want.\n![Snyk Org ID](https://github.com/snyk-labs/snyk-threadfix/blob/master/images/snyk-org-id-in-ui.png?raw=true)\n\n\nYou must also identify the Snyk project ID's for which you would like to generate ThreadFix data. You can do this using the Snyk API, for example, using the [List all projects](https://snyk.docs.apiary.io/#reference/projects/list-all-projects) endpoint. See also the [pysnyk SDK](https://github.com/snyk-labs/pysnyk). Another way of identifying the project IDs you want to use is simply by browsing to the desired project(s) with the Snyk UI and grabbing the UUID from the address bar of your browser.\n![Snyk Project ID](https://github.com/snyk-labs/snyk-threadfix/blob/master/images/project-id-in-snyk-ui.png?raw=true)\n\n\nOnce you have a project ID or list of project IDs that you would like to generate a threadfix file for, run the following:\n\n*For a single project ID:*\n```\nsnyk-threadfix --org-id=<your-snyk-org-id> --project-ids=<snyk-project-id>\n```\n\n*For multiple IDs:*\n```\nsnyk-threadfix --org-id=<your-snyk-org-id> --project-ids=<snyk-project-id-0>,<snyk-project-id-1>,<snyk-project-id-2>,...\n```\n\nThreadFix JSON data will be output to standard out. If you would like to save the JSON to a file you can either pipe it to a file or use the `--output` parameter, for example:\n```\nsnyk-threadfix --output=<your-desired-output-filename>.threadfix --org-id=<your-snyk-org-id> --project-ids=<snyk-project-id>\n```\n\n\nAdditional input parameters are available:\n```\nsnyk-threadfix --help\n```\n",
    'author': 'Jeff McLean',
    'author_email': 'jeff@snyk.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snyk-labs/snyk-threadfix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
