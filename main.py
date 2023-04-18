import click

from models.medium import post_article_from_file
from models.translate import translate_article


@click.group()
def cli():
    pass


@click.command()
@click.option('-ifn', '--input-filename', 'input_filename', help='input filename')
def translation(input_filename: str):
    '''Translate article'''
    translate_article(input_filename)


cli.add_command(translation)

if __name__ == '__main__':
    cli()
