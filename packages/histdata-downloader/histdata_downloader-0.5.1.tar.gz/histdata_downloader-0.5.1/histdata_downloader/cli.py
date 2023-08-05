# -*- coding: utf-8 -*-

"""Console script for histdata_downloader."""
import sys
import logging
import click

from histdata_downloader.histdata_downloader import SetDownloader
from histdata_downloader.tui import TestApp
from histdata_downloader.logger import log_setup

logger = logging.getLogger(__name__)


@click.group()
@click.option("--verbosity", "-v", default='INFO')
def main(verbosity):
    """Console script for histdata_downloader."""
    log_setup(verbosity, 'activity.log')
    return 0

@main.command()
@click.option("--type", '-t',
              default='M1',
              type=click.Choice(['M1', 'ticks'], case_sensitive=False))
@click.option('--date-start', '-ds', required=True,
              type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--date-end', '-de', required=True,
              type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--instruments', '-i', required=True, multiple=True)
@click.option('--output-path', '-o', required=True,
              type=click.Path(exists=False))
@click.option('--tqdm', default=False, is_flag=True)
def download(**kwargs):
    logger.debug('calling download command with args %s', kwargs)
    downloader = SetDownloader(kwargs)
    downloader.run()
    logger.info("Download complete !")


@main.command()
def tui():
    logger.debug("calling tui command.")
    app = TestApp()
    app.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
