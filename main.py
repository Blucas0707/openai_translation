import click

from models.translate import translate_article


@click.group()
def cli():
    pass


@cli.command()
@click.option('-ifn', '--input-filename', 'input_filename', help='input filename')
def translation(input_filename: str):
    '''Translate article'''
    translate_article(input_filename)


if __name__ == '__main__':
    cli()
