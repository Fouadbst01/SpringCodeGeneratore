import click
import questionary
from os import mkdir,getcwd,path,remove
import requests as req
import zipfile

@click.group()
def sg():
    pass

@click.command()
@click.argument("project_name")
def create(project_name):

    package_name = questionary.text(
        'package name ? (com.exemple)',default='com.exemple'
    ).ask()

    artifact_id = questionary.text(
        f'artifact_id ? ({project_name})',default=project_name
    ).ask()


    packaging= questionary.select(
        'Select packaging ? (JAR)',
        choices=[
            "jar",
            "war",
        ],
        default="jar").ask()

    dbpack= questionary.select(
        'Select pckages',
        choices=[
            "MySql",
            "H2",
            "MongoDB", 
        ]).ask()
    
    depe= questionary.checkbox(
        'select dependencies',
        choices=[
            "Lambok",
            "Web",
            "data-jpa"
        ],
     ).ask()

    
    url = "https://start.spring.io/starter.zip?type=maven-project&language=java&bootVersion=2.7.1&baseDir="+project_name+"&groupId="+package_name+"&artifactId="+artifact_id+"&name="+project_name+"&packageName="+package_name+"."+project_name+"&packaging="+packaging+"&javaVersion=1.8&dependencies=web,lombok,data-jpa,mysql"
    
    file = req.get(url, allow_redirects=True)

    pack_dir_name = package_name.split('.')
   
    project_file_name = project_name+".zip"
    open(project_file_name, 'wb').write(file.content)
    with zipfile.ZipFile(project_file_name, 'r') as zip_ref:
        zip_ref.extractall()
    
    remove(path.join(getcwd(),project_file_name))
    
    mypath=path.join(getcwd(),project_name,"src","main","java",*pack_dir_name,project_name)
    
    listdir = ["entities","dtos","enums","repositories","services","web","mappers"]
    for dir in listdir:
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
