import click

from models.translate import base as translate_m


@click.group()
def cli():
    pass


@cli.command()
@click.option("-sp", "--source-path", "source_path", help="input source path")
def translate(source_path: str):
    """Translate article"""
    translate_m.translate(source_path)


@cli.command()
@click.option("-sp", "--source-path", "source_path", help="input source path")
def transcribe(source_path: str):
    """Transcribe File from given source path"""
    translate_m.transcribe(source_path)


if __name__ == "__main__":
    cli()
