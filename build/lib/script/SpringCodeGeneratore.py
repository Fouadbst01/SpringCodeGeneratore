from audioop import add
import curses
import sys
from typing import List, Text
import zipfile

from pyparsing import Char
from os.path import exists
from os import mkdir, getcwd, walk, scandir,remove
import requests as req

class1 = ["id","String", "int", "double","Long","Date"]
class2 = ["String","Long"]
class3 = ["ManyToMany","ManyToOne","OneToOne","OneToMany"]

classes =class1

mypath=""

def choseType(stdscr):
    attributes = {}
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    attributes['normal'] = curses.color_pair(1)

    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['highlighted'] = curses.color_pair(2)

    c = 0 
    option = 0 
    while c != 10:
        stdscr.erase()
        for i in range(len(classes)):
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            stdscr.addstr("> ")
            stdscr.addstr(classes[i] + '\n', attr)
        c = stdscr.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(classes) - 1:
            option += 1

    stdscr.addstr(classes[option])
    return classes[option];

#curses.wrapper(choseType)
def start(args):
    match args:
        case 'g':
            generateProjectStructure()
        case 'c':
            return addEntity(sys.argv[2])
        case 'r':
            return GenerateRepositorise()
        case 'b':
            return basePackage(sys.argv[2])
        case 'i':
            return init(sys.argv[2])
        case 'a':
            return addAssociation()

def basePackage(arg):
    cont=1
    if(arg==""):
        mpath = getcwd()+"/src/main/java/"
    else:
        mpath = getcwd()+"/"+arg+"/src/main/java/"
    flag=True
    while flag:
        list = [f.path for f in scandir(mpath) if f.is_dir()]
        if(cont<4 and len(list)!=0):
            mpath=list[0]
        else:
            flag=False
        cont=cont+1
    return mpath

def addEntity(name):
    global mypath
    mypath = basePackage("")
    list= mypath.split("/")
    pname=list[len(list)-1]
    if(exists(name+".java")):
        print("Entity alerady existe !!")
        return
    if(not exists(mypath+"/entities")):
        mkdir(mypath+"/entities")
    print(mypath)
    f = open(mypath+"/entities/"+name+".java", "w")

    fdto = open(mypath+"/dtos/"+name+"DTO"+".java","w")

    fdto.write(
        "package com.enset."+pname+".dtos;\n\n"
        +"import lombok.Data;\n"
        +"import java.util.Date;\n"
        +"\n\n@Data\n"
        +"public class "+name+"DTO {\n"
    )

    f.write("package com.enset."+pname+".entities;\n\n"+"import lombok.AllArgsConstructor;\n"
+"import lombok.Data;\n"
+"import lombok.NoArgsConstructor;\n"
+"import javax.persistence.Entity;\n"
+"import javax.persistence.GeneratedValue;\n"
+"import java.util.Date;\n"
+"import javax.persistence.GenerationType;\n"
+"import javax.persistence.Id;\n"
+"import javax.persistence.*;\n import java.util.List;"
+"\n\n@Data\n"+
"@AllArgsConstructor\n@NoArgsConstructor\n"+
"@Entity\n"+
"public class "+name+"{\n")
    while(1):
        print("filed name > ",end="")
        filedname= input()
        if filedname=="":
            break
        print("fild type > ",end="")
        filedtype=curses.wrapper(choseType)
        if(filedtype=='id'):
            global classes
            classes=class2
            print("id type :")
            idType= curses.wrapper(choseType)
            f.write("\t@Id")
            if(idType=="Long"):
                f.write("@GeneratedValue(strategy = GenerationType.IDENTITY)\n")
            else:
                f.write("\n")
            f.write("\tpublic "+idType+" "+filedname+";\n")
            fdto.write("\tpublic "+idType+" "+filedname+";\n")     
            classes=class1
            continue
        if(filedtype=='Date'):
            f.write("\t@Temporal(TemporalType.DATE)\n")
            f.write("\tpublic Date "+filedname+";\n")
            fdto.write("\tpublic Date "+filedname+";\n") 
            continue
        print(filedtype)
        f.write("\tpublic "+filedtype+" "+filedname+";\n")
        fdto.write("\tpublic "+filedtype+" "+filedname+";\n")
    f.write("}")
    fdto.write("}")
    f.close()
    fdto.close()

def generateProjectStructure():
    try:
        if(not exists(mypath+"/entities")):
            print(mypath+"/entities")
            mkdir(mypath+"/entities")
        if(not exists(mypath+"/main/dtos")):
            mkdir(mypath+"/dtos")
        if(not exists(mypath+"/enums")):
            mkdir(mypath+"/enums")
        if(not exists(mypath+"/repositories")):
            mkdir(mypath+"/repositories")
        if(not exists(mypath+"/services")):
            mkdir(mypath+"/services")
        if(not exists(mypath+"/web")):
            mkdir(mypath+"/web")
        if(not exists(mypath+"/dtos")):
            mkdir(mypath+"/dtos")
    except OSError as err:
        print("alerady generated !!")

def GenerateRepositorise():
    mypath = basePackage("")
    list= mypath.split("/")
    pname=list[len(list)-1]
    for subdir, dirs, files in walk(mypath+"/entities"):
        for file in files:
            entityName=file.partition('.')[0]
            f = open(mypath+'/entities/'+entityName+".java", 'r')
            idType=""
            flag=False
            while True:
                str=f.readline()
                if('@Id' in str):
                    flag=True
                    idType=f.readline().split(" ")[1]
                    break
            if(flag and not exists(mypath+"/repositories/"+entityName+"Repository.java")):
                f = open(mypath+"/repositories/"+entityName+"Repository.java", "w")
                f.write("package com.enset."+pname+".repositories;\n\n"+
                        "import com.enset."+pname+".entities."+entityName+";\n"
                        +"import org.springframework.data.jpa.repository.JpaRepository;\n"
                        +"import org.springframework.stereotype.Repository;\n\n"
                        +"@Repository\n"
                        +"public interface "+entityName+"Repository extends JpaRepository<"
                        +entityName
                        +","+idType+"> {\n}")
            else:
                print("id dosent existe")
            f.close()

def init(arg):
    global mypath
    url = "https://start.spring.io/starter.zip?type=maven-project&language=java&bootVersion=2.7.0&baseDir="+arg+"&groupId=com.enset&artifactId="+arg+"&name="+arg+"&description=Demo%20project%20for%20Spring%20Boot&packageName=com.enset."+arg+"&packaging=jar&javaVersion=1.8&dependencies=web,lombok,data-jpa,mysql"
   
    file = req.get(url, allow_redirects=True)
    open(arg+".zip", 'wb').write(file.content)
    with zipfile.ZipFile(arg+".zip", 'r') as zip_ref:
        zip_ref.extractall()
    remove(arg+".zip")
    mypath = basePackage(arg)
    print("enter DB name > ")
    dbname=input()
    f= open("./"+arg+"/src/main/resources/application.properties","w")
    f.write("spring.datasource.url=jdbc:mysql://localhost:3306/"+dbname+"?createDatabaseIfNotExist=true\n")
    f.write("spring.datasource.username=root\n")
    f.write("spring.datasource.password=\n")
    #f.write("spring.jpa.show-sql=true")
    f.write("spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect\n")
    f.write("spring.jpa.hibernate.ddl-auto=update\n")
    f.close()
    generateProjectStructure()

def addAssociation():
    mypath = basePackage("")
    mypath=mypath+"/entities"
    global classes
    listE=list() 
    for subdir, dirs, files in walk(mypath):
        for file in files:
            listE.append(file.split(".")[0])

    print("chose first entity > ",end="")
    classes=listE
    entityOne=curses.wrapper(choseType)
    print(entityOne)
    classes=class3
    chosen=curses.wrapper(choseType)
    classes=listE
    print("chose first entity > ",end="")
    entityTow=curses.wrapper(choseType)
    print(entityTow)
    AddDependency(chosen,entityOne,entityTow)

    
def AddDependency(chosen,entity1,entity2):
    match chosen:
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
            str1="\t@ManyToOne\n"+dto1
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
    mypath = basePackage("")
    list= mypath.split("/")
    pname=list[len(list)-1]
    write_in_end(mypath+"/entities",entity,str)
    write_in_end(mypath+"/dtos",entity+"DTO",dto,True)


def write_in_end(path,entity,str,flag=False):
    
    with open(path+"/"+entity+".java", 'r+') as file:
        lines = file.readlines()
        file.seek(0,0)
        for i in range(len(lines)):
            if(i==2 and flag):
                file.write("\nimport java.util.List;\n")
            if(i==len(lines)-1):
                file.write(str)
            file.write(lines[i])
        file.close()

def main():
    global arg
    arg = Char(sys.argv[1])
    start(arg)

if __name__ == "__main__":
    main()

