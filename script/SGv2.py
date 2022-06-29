import click

@click.group()
def sg():
    pass

@click.command()
def init():
    click.echo('Initialization')

@click.command()
def doSo():
    click.echo('do somrthings')

sg.add_command(init)
sg.add_command(doSo)

if __name__ == "__main__":
    print("yesyyyyyy")
    sg()