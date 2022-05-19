import curses
import sys

from pyparsing import Char
from os.path import exists
from os import mkdir, walk

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
            #stdscr.addstr("{0}. ".format(i + 1))
            stdscr.addstr("> ")
            stdscr.addstr(classes[i] + '\n', attr)
        c = stdscr.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(classes) - 1:
            option += 1

    stdscr.addstr(classes[option])
    return classes[option];
    #stdscr.getch()

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

def basePackage(arg):
    _FilePath=arg.replace(".","/")
    _FilePath+="/src/main"
    if(not exists(_FilePath)):
        print("incorrect base package !!")
    print(_FilePath)

def addEntity(name):
    print(name+".java")
    if(exists(name+".java")):
        print("Entity alerady existe !!")
        return
    if(not exists("./src/main/entities")):
        mkdir("./src/main/entities")

    f = open("./src/main/entities/"+name+".java", "w")
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
    if(not exists("./src/main/entities")):
        mkdir("./src/main/entities")
    if(not exists("./src/main/dtos")):
        mkdir("./src/main/dtos")
    if(not exists("./src/main/enums")):
        mkdir("./src/main/enums")
    if(not exists("./src/main/repositories")):
        mkdir("./src/main/repositories")
    if(not exists("./src/main/services")):
        mkdir("./src/main/services")
    if(not exists("./src/main/web")):
        mkdir("./src/main/web")

def GenerateRepositorise():
    for subdir, dirs, files in walk("./src/main/entities"):
        for file in files:
            entityName=file.partition('.')[0]
            #flag=False
            #with open('./src/main/entities/'+entityName+".java") as f:
            f = open('./src/main/entities/'+entityName+".java", 'r')
            idType=""
            while True:
                str=f.readline()
                if(str and 'ID' in str):
                    idType=f.readline().split(" ")[1]
                    break
            if(not exists("./src/main/repositories/"+entityName+"Repository.java")):
                f = open("./src/main/repositories/"+entityName+"Repository.java", "w")
                f.write("import org.springframework.data.jpa.repository.JpaRepository;\n"
                        +"import org.springframework.stereotype.Repository;\n\n"
                        +"@Repository\n"
                        +"public interface "+entityName+"Repository extends JpaRepository<"
                        +entityName
                        +","+idType+"> {\n}")
            f.close()


arg = Char(sys.argv[1])
start(arg)