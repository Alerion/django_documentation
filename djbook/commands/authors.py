import logging
import os

from cliff.command import Command as BaseCommand
from jinja2 import Environment, FileSystemLoader
from github import GithubException

from djbook.cliff_utils import GithubCommandMixin


class Command(GithubCommandMixin, BaseCommand):
    """
    Generate page with authors from git history
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        repo = self.get_repo(self.app.repo_name)

        try:
            self.save_to_file({
                'contributors': repo.get_contributors()
            })
        except GithubException as e:
            print(e)

    def save_to_file(self, context):
        env = Environment(loader=FileSystemLoader(self.app.templates_path))
        template_name = 'authors.html'
        template = env.get_template(template_name)
        with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
            output.write(template.render(**context).encode('utf8'))
