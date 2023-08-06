#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

@click.command()
@click.option('--name', '-n', default='World')
def cmd(name):
    msg = 'Hello, {name}!'.format(name=name)
    click.echo(msg)

def main():
    cmd()

if __name__ == '__main__':
    main()
