from ast import alias
from copyreg import constructor
import click
from click_aliases import ClickAliasedGroup
import questionary
from os import mkdir,getcwd,path,remove,scandir,walk
import requests as req
import zipfile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@click.group(cls=ClickAliasedGroup)
def sg():
    pass

@sg.command(aliases=['c'])
@click.argument("project_name")
def create(project_name):
    if(path.isdir(path.join(getcwd(),project_name))):
        raise SystemExit(f"{bcolors.FAIL}Eroor: Project name already exists")
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
            "mysql",
            "h2",
            #"MongoDB", 
        ]).ask()
    
    db_name = questionary.text(
        'database name ?'
    ).ask()

    
    depe= questionary.checkbox(
        'select dependencies',
        choices=[
            "lombok",
            "web",
            "data-jpa"
        ],
     ).ask()

    depe = ",".join(depe)

    package = depe+","+dbpack

    

    url = "https://start.spring.io/starter.zip?type=maven-project&language=java&bootVersion=2.7.5&baseDir="+project_name+"&groupId="+package_name+"&artifactId="+artifact_id+"&name="+project_name+"&packageName="+package_name+"."+project_name+"&packaging="+packaging+"&javaVersion=1.8&dependencies="+package

    print(url)
    
    file = None
    try :
        file = req.get(url, allow_redirects=True)
        print("file :")
        print(file)
    except req.exceptions.HTTPError as errh:
        print (f"{bcolors.FAIL}Http Error:",errh)
        SystemExit(-1)
    except req.exceptions.ConnectionError as errc:
        print (f"{bcolors.FAIL}Error Connecting:",errc)
        SystemExit(-1)
    except req.exceptions.Timeout as errt:
        print (f"{bcolors.FAIL}Timeout Error:",errt)
        SystemExit(-1)
    except req.exceptions.RequestException as err:
        print (f"{bcolors.FAIL}OOps: Something Else",err)
        SystemExit(-1)

    if(file !=None):
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
    f= open( path.join(getcwd(),project_name,"src","main","resources","application.properties"),"w")
    if(dbpack == "mysql"):
        f.write("spring.datasource.url=jdbc:mysql://localhost:3306/"+db_name+"?createDatabaseIfNotExist=true\n")
        f.write("spring.datasource.username=root\n")
        f.write("spring.datasource.password=\n")
        #f.write("spring.jpa.show-sql=true")
        f.write("spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect\n")
        f.write("spring.jpa.hibernate.ddl-auto=create\n")
        f.write("server.port=8083")
    if(dbpack == "h2"):
        f.write("spring.datasource.url=jdbc:h2:mem:"+db_name)
        f.write("\nspring.h2.console.enabled=true")
    f.close()
        

@sg.command(aliases=['e'])
@click.argument("entity_name")
def entity(entity_name):
    my_path = getBasePath()
    entities_path = path.join(my_path,"entities")
    dtos_path = path.join(my_path,"dtos")

    entity_name = entity_name.capitalize()

    entity_file_path = path.join(entities_path,entity_name+".java")
    dto_file_path = path.join(dtos_path,entity_name+"DTO"+".java")

    if(path.exists(entity_file_path)):
        print (f"{bcolors.FAIL}Entity alerady existe !!")
        SystemExit(-1)

    entity_file = open(entity_file_path, "w")

    dto_file = open(dto_file_path,"w")

    package = getBase()

    dto_file.write(
        "package "+ package+".dtos;\n\n"
        +"import lombok.Data;\n"
        +"import java.util.Date;\n"
        +"\n\n@Data\n"
        +"public class "+entity_name+"DTO"+" {\n"
    )

    entity_file.write("package "+package+".entities;\n\n"+"import lombok.AllArgsConstructor;\n"
        +"import lombok.Data;\n"
        +"import lombok.NoArgsConstructor;\n"
        +"import javax.persistence.Entity;\n"
        +"import javax.persistence.GeneratedValue;\n"
        +"import java.util.Date;\n"
        +"import javax.persistence.GenerationType;\n"
        +"import javax.persistence.Id;\n"
        +"import javax.persistence.*;\nimport java.util.List;"
        +"\n\n@Data\n"+
        "@AllArgsConstructor\n@NoArgsConstructor\n"+
        "@Entity\n"+
        "public class "+entity_name+"{\n")
    
    while(1):
        filed_name = questionary.text(
        'filed name : '
        ).ask()
        
        if filed_name=="":
            break
        filed_type = questionary.select(
        'fild type ?',
        choices=[
            "id","String", "int","short","float","double","long","Date" 
        ]).ask()
    
        if(filed_type =='id'):
            id_type = questionary.select(
            'id type ?',

            choices=[
                "long","String"
            ]).ask()

            entity_file.write("\t@Id")
            if(id_type=="long"):
                entity_file.write("@GeneratedValue(strategy = GenerationType.IDENTITY)\n")
            else:
                entity_file.write("\n")
            entity_file.write("\tprivate "+id_type+" "+filed_name+";\n")
            dto_file.write("\tprivate "+id_type+" "+filed_name+";\n")     
            continue

        if(filed_type=='Date'):
            entity_file.write("\t@Temporal(TemporalType.DATE)\n")
            entity_file.write("\tprivate Date "+filed_name+";\n")
            dto_file.write("private Date "+filed_name+";\n") 
            continue

        entity_file.write("\tprivate "+filed_type+" "+filed_name+";\n")
        dto_file.write("\tprivate "+filed_type+" "+filed_name+";\n")

    entity_file.write("}")
    dto_file.write("}")
    entity_file.close()
    dto_file.close()

@sg.command(aliases=['r'])
def repositories():
    my_path = getBasePath()
    repositories_path = path.join(my_path,"repositories")
    entities_path = path.join(my_path,"entities")

    package = getBase()

    for subdir, dirs, files in walk(entities_path):
        for file in files:
            entity_name=file.partition('.')[0]
            f = open(path.join(entities_path,file), 'r')
            idType=""
            flag=False
            while True:
                str=f.readline()
                if not str:
                    break
                if('@Id' in str):
                    flag=True
                    idType=f.readline().split(" ")[1]
                    break
            if(flag and not path.exists(path.join(repositories_path,entity_name+"Repository.java"))):
                f = open(path.join(repositories_path,entity_name+"Repository.java"), "w")
                f.write("package "+package+".repositories;\n\n"+
                        "import "+package+".entities."+entity_name+";\n"
                        +"import org.springframework.data.jpa.repository.JpaRepository;\n"
                        +"import org.springframework.stereotype.Repository;\n\n"
                        +"@Repository\n"
                        +"public interface "+entity_name+"Repository extends JpaRepository<"
                        +entity_name
                        +","+idType+"> {\n}")
            else:
                print(f"{bcolors.FAIL}Faild to generate "+entity_name+"Repository : id dosent existe")
            f.close()


@sg.command()
@click.argument("enum_name")
def enum(enum_name):
    enum_name = enum_name.capitalize()
    str="public enum "+enum_name.capitalize()+" {\n";
    values = []
    while(1):
        value = questionary.text(
        'Enter Value : '
        ).ask()

        if value==None or value=="":
            break

        values.append(value.upper())

    str=str+",".join(values)+"\n}"

    my_path = getBasePath()
    repositories_path = path.join(my_path,"enums")

    with open(path.join(repositories_path,enum_name+".java"),"w") as f:
        f.write(str)
        f.close()

@sg.command(aliases=['a'])
def association():
    my_path = getBasePath()

    entities_path = path.join(my_path,"entities")
    list_entity=[]
    for subdir, dirs, files in walk(entities_path):
        for file in files:
            list_entity.append(file.split(".")[0])
    

    first_entity = questionary.select(
        'first entity :',
        choices=
            list_entity 
        ).ask()

    association_type = questionary.select(
        'first entity :',
        choices=["ManyToMany","ManyToOne","OneToOne","OneToMany"]).ask()


    second_entity = questionary.select(
        'second entity',
        choices=
            list_entity 
        ).ask()
    
    AddDependency(association_type,first_entity,second_entity)

def AddDependency(association_type,entity1,entity2):
    match association_type:
        case "OneToMany": 
            dto1="\t"+"List<"+entity2+"DTO>"+" list"+entity2+"DTO;\n"
            str1='\t@OneToMany(mappedBy = "'+entity1.lower()+'",fetch = FetchType.LAZY)\n'+"\t"+"List<"+entity2+">"+" list"+entity2+";\n"
            dto2="\t"+entity1+"DTO "+entity1.lower()+"DTO;\n"
            str2="\t@ManyToOne\n"+"\t"+entity1+" "+entity1.lower()+";\n"
            write(str1,entity1,dto1)
            write(str2,entity2,dto2)
        case "ManyToOne":
            dto2="\t"+"List<"+entity1+"DTO>"+" list"+entity1+"DTO;\n"
            str2='\t@OneToMany(mappedBy = "'+entity2.lower()+'",fetch = FetchType.LAZY)\n'+"\t"+"List<"+entity1+">"+"list"+entity1+";\n"
            dto1="\t"+entity2+"DTO "+" "+entity2.lower()+"DTO;\n"
            str1="\t@ManyToOne\n\t"+entity2+" "+entity2.lower()+";\n"
            write(str1,entity1,dto1)
            write(str2,entity2,dto2)
        case "OneToOne":
            dto1="\t"+entity2+"DTO "+entity2.lower()+"DTO"+";\n"
            str1="\t@OneToOne\n"+"\t"+entity2+" "+entity2.lower()+";\n"
            dto2="\t"+entity1+"DTO "+entity1.lower()+"DTO"+";\n"
            str2="\t@OneToOne\n"+"\t"+entity1+" "+entity1.lower()+";\n"
            write(str1,entity1,dto1)
            write(str2,entity2,dto2)
        case "ManyToMany":
            dto1="\tList<"+entity1+"DTO> list"+entity1+"DTO"+";\n"
            str1="\t@ManyToMany\n"+"\t"+"List<"+entity1+"> list"+entity1+";\n"
            dto2="\tList<"+entity2+"DTO> list"+entity2+"DTO"+";\n"
            str2="\t@ManyToMany\n"+"\t"+"List<"+entity2+"> list"+entity2+";\n"
            write(str1,entity1,dto1)
            write(str2,entity2,dto2)

def write(str,entity,dto):
    my_path = getBasePath()
    entities_path = path.join(my_path,"entities")
    dtos_path = path.join(my_path,"dtos")
    write_in_end(path.join(entities_path,entity),str)
    write_in_end(path.join(dtos_path,entity+"DTO"),dto,True)


def write_in_end(path,str,flag=False):
    
    with open(path+".java", 'r+') as file:
        lines = file.readlines()
        file.seek(0,0)
        for i in range(len(lines)):
            if(i==2 and flag):
                file.write("\nimport java.util.List;\n")
            if(i==len(lines)-1):
                file.write(str)
            file.write(lines[i])
        file.close()

def getBasePath():

    dir_name = path.basename(getcwd())

    my_path = path.join(getcwd(),"src","main","java")
    if(path.exists(my_path)):
        while True:
            list = [f.path for f in scandir(my_path) if f.is_dir()]
            tmp_dir_name = path.basename(list[0])
            my_path = path.join(my_path,tmp_dir_name)
            if(tmp_dir_name == dir_name):
                break;
        return my_path;
    else:
        print (f"{bcolors.FAIL}OOps: access to project folder to execute this commande 'cd MyProgect'")
        SystemExit(-1)

def getBase():

    dir_name = path.basename(getcwd())

    my_path = path.join(getcwd(),"src","main","java")

    package_list = []
    if(path.exists(my_path)):
        while True:
            list = [f.path for f in scandir(my_path) if f.is_dir()]
            tmp_dir_name = path.basename(list[0])
            package_list.append(tmp_dir_name)
            my_path = path.join(my_path,tmp_dir_name)
            if(tmp_dir_name == dir_name):
                break;
        return ".".join(package_list);
    else:
        print (f"{bcolors.FAIL}OOps: access to project folder to execute this commande 'cd MyProgect'")
        SystemExit(-1)




#add commande to group
#sg create
sg.add_command(create)

ALIASES={
    "cr" : create,
}

def main():
    sg()
