"""
Copyright 2019, NIA(정보화진흥원), All rights reserved.
Mail : rocketgrowthsj@publicai.co.kr
"""
import click
from textaug.core import multiprocess_image_augumentation


@click.command()
@click.argument('input_dir', required=True,
                type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=str))
@click.argument('output_dir', required=True,
                type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=str))
@click.option('--multiples', required=False, default=1)
@click.option('--blur', required=False, default=5.)
@click.option('--noise', required=False, default=30.)
@click.option('--strength', required=False, default=.2)
@click.option('--scale', required=False, default=.1)
@click.option('--rotate', required=False, default=10)
@click.option('--shear', required=False, default=5.)
@click.option('--elastic', required=False, default=.7)
def cli(input_dir, output_dir, multiples, blur, noise, strength,
        scale, rotate, shear, elastic):
    """
    :param input_dir:
    :param output_dir:
    :param multiples:
    :param blur:
    :param noise:
    :param strength:
    :param scale:
    :param rotate:
    :param shear:
    :param elastic:
    :return:
    """
    multiprocess_image_augumentation(
        input_dir,
        output_dir,
        multiples,
        blur,
        noise,
        strength,
        scale,
        rotate,
        shear,
        elastic)


if __name__ == "__main__":
    # Argument parsing
    cli()