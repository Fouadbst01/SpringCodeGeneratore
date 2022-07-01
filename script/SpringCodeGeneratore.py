import click
from os import mkdir,getcwd,path

@click.group()
def sg():
    pass

@click.command()
@click.argument("name")
def create(name):
    click.Choice(["hzhzhzh","ooozozoz","izhezioah"])
    mypath=path.join(getcwd(),name)
    mkdir(mypath)
    listdir = ["entities","dtos","enums","repositories","services","web","mappers"]
    for dir in listdir:
        #print(path.join(mypath,dir))
        mkdir(path.join(mypath,dir))


@click.command()
def doSo():
    click.echo('do somrthings')

#add commande to group
#sg create
sg.add_command(create)
sg.add_command(doSo)

def main():
    sg()
