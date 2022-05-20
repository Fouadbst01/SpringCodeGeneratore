import curses
from itertools import count
import sys
from pexpect import EOF

from pyparsing import Char
from os.path import exists
from os import mkdir, walk, scandir,getcwd


class1 = ["String", "int", "double","Long", "id"]
class2 = ["String","Long"]
classes =class1

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

def basePackage():
    cont=1
    mpath = "./src/"
    flag=True
    while flag:
        list = [f.path for f in scandir(mpath) if f.is_dir()]
        if(cont<6 and len(list)!=0):
            mpath=list[0]
        else:
            flag=False
        cont=cont+1
    return mpath

def addEntity(name):
    print(name+".java")
    if(exists(name+".java")):
        print("Entity alerady existe !!")
        return
    if(not exists(mypath+"/entities")):
        mkdir(mypath+"/entities")

    f = open(mypath+"/entities/"+name+".java", "w")
    f.write("import lombok.AllArgsConstructor;\n"
+"import lombok.Data;\n"
+"import lombok.NoArgsConstructor;\n"
+"import javax.persistence.Entity;\n"
+"import javax.persistence.GeneratedValue;\n"
+"import javax.persistence.GenerationType;\n"
+"import javax.persistence.Id;\n"
+"\n\n@Data\n"+
"@AllArgsConstructor\n@NoArgsConstructor\n"+
"@Entity\n"+
"public class"+name+"{\n")
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
                f.write(" @GeneratedValue(strategy = GenerationType.IDENTITY)\n")
            else:
                f.write("\n")
            f.write("\tpublic "+idType+" "+filedname+";\n")
            classes=class1
            continue
        print(filedtype)
        f.write("\tpublic "+filedtype+" "+filedname+";\n")
    f.write("}")
    f.close()

def generateProjectStructure():
    try:
        if(not exists(mypath+"/entities")):
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
    except OSError as err:
        print("alerady generated !!")

def GenerateRepositorise():
    for subdir, dirs, files in walk(mypath+"/entities"):
        for file in files:
            entityName=file.partition('.')[0]
            print(entityName)
            f = open(mypath+'/entities/'+entityName+".java", 'r')
            idType=""
            flag=False
            while True:
                str=f.readline()
                if(str and 'ID' in str):
                    flag=True
                    print
                    idType=f.readline().split(" ")[1]
                    break
                print(str)
            if(flag and not exists(mypath+"/repositories/"+entityName+"Repository.java")):
                f = open(mypath+"/repositories/"+entityName+"Repository.java", "w")
                f.write("import org.springframework.data.jpa.repository.JpaRepository;\n"
                        +"import org.springframework.stereotype.Repository;\n\n"
                        +"@Repository\n"
                        +"public interface "+entityName+"Repository extends JpaRepository<"
                        +entityName
                        +","+idType+"> {\n}")
            else:
                print("id dosent existe")
            f.close()

print("** "+getcwd())
arg = Char(sys.argv[1])
mypath = basePackage()
#start(arg)
