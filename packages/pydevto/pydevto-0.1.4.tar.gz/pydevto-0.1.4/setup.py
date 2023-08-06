# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydevto']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8,<5.0', 'requests>=2.22,<3.0', 'six>=1.12,<2.0']

setup_kwargs = {
    'name': 'pydevto',
    'version': '0.1.4',
    'description': 'Unofficial dev.to api for python',
    'long_description': '# PyDevTo\n\nUnofficial dev.to api for python.\n\n### Features\n* Implements all endpoints from https://docs.dev.to/api/\n* Implements a few other api endpoints not documented but available in the source, such as users and follow_suggestions\n* Includes a helper method to convert html to dev.to specific markdown, including support for dev.to specific embeds such as YouTube.\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install pydevto.\n\n```bash\npip install pydevto\n```\n\n## Usage\n\nMake sure you have an api key to use the authenticated endpoints.  You can get your key from https://dev.to/settings/account\n(You can use pydevto without an api key for some functions, such as the public articles)\n\n```python\nimport pydevto\napi = pydevto.PyDevTo(api_key=\'MY_KEY\')\napi.articles()  # returns list of your own published articles\n```\n\n## Methods\n```python\nimport pydevto\napi = pydevto.PyDevTo(api_key=\'MY_KEY\')\napi.public_articles(page=None, tag=None, username=None, state=None, top=None)  # Return list of public (published) articles\napi.public_article(id)  # Return a single public (published) article given its id\napi.articles(page=None, per_page=None, state="published")  # Return a list of user articles\napi.create_article(...)  # Create an article\napi.update_article(id, ...)  # Update an article\napi.user(id=None, username=None)  # Return user information\napi.follow_suggestions(page=None)  # Return list of follow suggestions\napi.tags(page=None)  # Return list of tags\napi.webhooks()  # Return list of webhooks\napi.webhook(id)  # Return single webhook with id\napi.create_webhook(source, target_url, events)  # Create a new webhook\napi.delete_webhook(id)  # Delete  a webhook with id\n```\n\n## Html to Markdown\nPyDevTo contains a helper function to convert html to dev.to specific markdown (https://dev.to/p/editor_guide)\nIt supports images with captions using the HTML figcaption tag, and converts embeds such as YouTube to dev.to specific liquid tags.\n```python\n>>> import pydevto\n>>> pydevto.html_to_markdown(\'<h1>Heading</h1\') \n>>> \'# Heading\\n\\n\'\n>>> pydevto.html_to_markdown(\'<iframe src="https://www.youtube.com/embed/kmjiUVEMvI4"></iframe>\') \n>>> \'\\n{% youtube kmjiUVEMvI4 %}\\n\'  \n```\n\n## Known issues\n* The tags property does not currently work correctly when creating/updating an article.  There is an open issue report on dev.to for this.\n* The html to markdown only caters for a subset of embeds (YouTube, Twitter, repl.it, soundcloud and a few more), more will be added over time.\n\n## Contributing\nPull requests and issue reports are welcome.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': "'Loftie",
    'author_email': 'lpellis@gmail.com',
    'url': 'https://github.com/lpellis/pydevto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
