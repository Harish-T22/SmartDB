import speech_recognition as sr
import pyttsx3
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="pass")
mycursor=mydb.cursor()
dbname= None
engine = pyttsx3.init()




def enableautocommit():
    global mycursor
    mycursor.execute("set autocommit=1")
    
def disableautocommit():
    global mycursor
    mycursor.execute("set autocommit=0")

def alldbs():
    global mycursor
    mycursor.execute("show databases")
    listdb=[]
    for i in mycursor:
        listdb.append(i[0])
    return listdb

def alltb():
    global mycursor
    mycursor.execute("show tables")
    listtb=[]
    for i in mycursor:
        listtb.append(i[0])
    return listtb

def createdb(dbname):
    global mycursor
    mycursor.execute("create database "+dbname)

def usedb(dbname):
    global mycursor
    mycursor.execute("use "+dbname)

def dropdb(dbname):
    global mycursor
    mycursor.execute("drop database "+dbname)
    
def connect_db(dbname):
    global mydb
    global mycursor
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="pass",database=dbname)
    mycursor=mycursor()

def createtb(tbname):
    global mycursor
    query="create table "+tbname+" ("
    nxtfield="yes"
    primary=0
    while(nxtfield=="yes"):
        print("Enter the field details")
        fname=input("Enter the Field name:")
        ftype=input("Enter the Field type:")
        fsize=int(input("Enter the Field size:"))
        key=input("Do you want to set any key(constraint) to this Field?:").lower()
        if (key=="yes"):
           keyval=input("Enter the Constraint:")
           
        null=input("Do you want to allow NULL values in this Field?(yes or no):").lower()
        
        default=input("Do you want to set any default value to this Field?:").lower()
          
        if(default=="yes"):
           defaultval=input("Enter the default value:")
        elif (ftype=="int" or ftype=="integer" and key !=""):
           autoinc=input("Do you want to set autoincrement to this Field?:")
            
        query+=fname+" "+ftype+" ("+str(fsize)+")"
        if (key=="yes"):
            query+=" "+keyval+" "
            key=""
        if (null=="no"):
            query+=" not null "
            nul=""
        if (default=="yes"):
            query+=" default "+defaultval+" "
            default=""
        if (autoinc=="yes"):
            query+=" auto_increment "
            autoinc=""
            
        
        nxtfield=input("Do you want to add another field?")
        if(nxtfield=="yes"):
            query+=","
    query+=")"
    print(query)
    mycursor.execute(query)
    print("Table has been Created successfully")
    mycursor.execute("desc "+tbname)
    for i in mycursor:
        print(i)

def altertb(tbname):
    global mycursor
    nxtfield="yes"
    query="alter table "+tbname+" "
    option=input("What do you want to do with ",tbname) 
    if("add" in option and "colum" in option):
        query+="add column ("
        while(nxtfield=="yes"):
            print("Enter the field details")
            fname=input("Enter the Field name:")
            ftype=input("Enter the Field type:")
            fsize=int(input("Enter the Field size:"))
            query+=fname+" "+ftype+" ("+str(fsize)+")"
            nxtfield=input("Do you want to add another field?")
            if(nxtfield=="yes"):
                   query+=","
        query+=")"
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)

 
    elif(("drop" in option or "delete" in option) and "colum" in option):
        query+="drop column "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to drop:")
            query+=fname
            nxtfield=input("Do you want to add another field?")
            if(nxtfield=="yes"):
                query+=",drop column "
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)

              
    elif(("modify" in option or "change" in option)and "colum" in option):
        query+="modify "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to modify:")
            ftype=input("Enter the Field type:")
            fsize=int(input("Enter the Field size:"))
            query+=fname+" "+ftype+" ("+str(fsize)+")"
            nxtfield=input("Do you want to modify another field?")
            if(nxtfield=="yes"):
                 query+=",modify "
        mycursor.execute(query)
        print("Table has been Modified successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)
              
    elif(("rename" in option and "colum" in option) or ("change name" in option and "colum" in option)):
        query+="rename column "
        while(nxtfield=="yes"):
            fname=input("Enter the Field name to rename:")
            newfname=input("Enter the new Field name:")
            query+=fname+" to "+newfname
            nxtfield=input("Do you want to rename another field?")
            if(nxtfield=="yes"):
                query+=",rename column "
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+tbname)
        for i in mycursor:
            print(i)
 
    elif("rename" in option ):
        newtbname=input("Enter the new Table name:")
        query+="rename "+newtbname
        mycursor.execute(query)
        print("Table has been Altered successfully")
        mycursor.execute("desc "+newtbname)
        for i in mycursor:
            print(i)

def droptb(tbname):
    global mycursor
    mycursor.execute("drop table "+tbname)

def truncatetb(tbname):
    global mycursor
    mycursor.execute("truncate table "+tbname)

def renametb(tbname,newtbname):
    global mycursor
    mycursor.execute("rename table "+tbname+" to "+newtbname)

def insertrec(tbname):
    global mycursor
    insnext="yes"
    query="insert into "+tbname+" values "
    mycursor.execute("desc "+tbname)
    mylist=list(mycursor)
    while(insnext=="yes"):
        for i in mylist:
            i0=str(i[0])
            i1=str(i[1])
            print("Enter value for the field "+i0+"("+i1[2:len(i1)-1]+"):")
            value=input()
            if (mylist.index(i)==0):
                query+="("
            if ("varchar" in i1):
                query+="'"+value+"'"
            else:
                query+=value
            if (mylist.index(i)!=len(mylist)-1):
                query+=","
            else:    
                query+=")"
        insnext=input("Do you want to insert another record?")
        if(insnext=="yes"):
            query+=","
    mycursor.execute(query)

def updaterec(tbname):
    global mycursor
    quotation=0
    updnext="yes"
    query="update "+tbname+" set "
    mycursor.execute("desc "+tbname)
    mylist=list(mycursor)
    fieldlist=[]
    for i in mylist:
        fieldlist.append(i[0])
    
    while(updnext=="yes"):
        fname=input("Enter the Field name:")
        while(fname not in fieldlist):
            print("Sorry, there is no Field with name ",fname)
            fname=input("Enter the Field name:")
        else:
            fval=input("Enter the value to update:")
            query+=fname+"="
            for i in mylist:
                if (i[0]==fname and "varchar" in str(i[1])):
                    query+="'"
                    quotation=1
            query+=fval
            if (quotation==1):
                query+="'"
                quotation=0
        updnext=input("Do you want to update any other?:")
        if(updnext=="yes"):
            query+=","
    condfield=input("Which record(s) you want to update? give condition")
    query+=" where "+condfield
    mycursor.execute(query)

def selectrec(tbname,selallrec,selallfield):
    global mycursor
    if(selallrec=="yes" and selallfield=="yes"):
        query="select * from "+tbname
    elif(selallfield=="yes"):
        query="select * from "+tbname+" where "
        condfield=input("Which record(s) you want to display? give condition")
        query+=condfield
    elif(selallrec=="yes"):
        query="select "
        nxtfield="yes"
        mycursor.execute("desc "+tbname)
        mylist=list(mycursor)
        fieldlist=[]
        for i in mylist:
           fieldlist.append(i[0])
        while(nxtfield=="yes"):
           fname=input("Enter the Field name:")
           while(fname not in fieldlist):
             print("Sorry, there is no Field with name ",fname)
             fname=input("Enter the Field name:")
           query+=fname
           nxtfield=input("Do you want to display another Field?:")
           if(nxtfield=="yes"):
              query+=","
        query+=" from "+tbname
    else:
        query="select "
        nxtfield="yes"
        mycursor.execute("desc "+tbname)
        mylist=list(mycursor)
        fieldlist=[]
        for i in mylist:
           fieldlist.append(i[0])
        while(nxtfield=="yes"):
           fname=input("Enter the Field name:")
           while(fname not in fieldlist):
             print("Sorry, there is no Field with name ",fname)
             fname=input("Enter the Field name:")
           query+=fname
           nxtfield=input("Do you want to display another Field?:")
           if(nxtfield=="yes"):
              query+=","
        query+=" from "+tbname+" where "
        condfield=input("Which record(s) you want to display? give condition")
        query+=condfield
    mycursor.execute(query)
    for i in mycursor:
        print(i)
    
def deleterec(tbname):
    global mycursor
    query="delete from "+tbname+" where "
    condfield=input("Which record(s) you want to delete? give condition")
    query+=condfield
    mycursor.execute(query)
def desctb(tbname):
    global mycursor
    mycursor.execute("desc "+tbname)
    for i in mycursor:
        print(i)
def commit():
    global mycursor
    mycursor.execute("commit")
    
    
    


enableautocommit()

 
def t2v(S):
  global engine
  engine.say(S)
  engine.runAndWait()
  
def v2t():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("I'm Listening")
    audio = r.listen(source)
  return (r.recognize_google(audio)).lower() 
   
print("Enter The SQL command\n")
command=v2t()
print(command)
while(command != "exit" and command != "quit" and command != "bye"):
  
  #create database
  if "create" in command and "database" in command:
      print("Enter the Database Name:")
      t2v("Enter the Database Name")
      dbname=input()
      listdb=alldbs()
      if dbname in listdb:
          print("Sorry The Database",dbname," already exists.please Enter a different name")
          t2v("Sorry The Database"+dbname+" already exists.please Enter a different name")
      else:
          createdb(dbname)
          print("Database ",dbname," has been Created Successfully and you are currently using it")
          t2v("Database "+dbname+" has been Created Successfully and you are currently using it")
          connect_db(dbname)
          listdb=alldbs()
          for i in listdb:
              print(i)
              
  #end of create database
  #use database
              
  elif (("select" in command or "use" in command) and "database" in command):
      print("Enter the Database Name:")
      t2v("Enter the Database Name")
      dbname=input()
      listdb=alldbs()
      if dbname not in listdb:
          print("Sorry The Database",dbname," does not exist.please Enter an existing Database name")
          t2v("Sorry The Database"+dbname+" does not exist.please Enter an existing Database name")
      else:
          usedb(dbname)
          print("Databse ",dbname," has been selected")
          t2v("Databse "+dbname+" has been selected")
          
  #end of use database
  #drop database
          
  elif (("delete" in command or "drop" in command) and "database" in command):
      print("Enter the Database Name:")
      t2v("Enter the Database Name")
      dbname=input()
      listdb=alldbs()
      if dbname not in listdb:
          print("Sorry The Database",dbname," does not exist.please Enter an existing Database name")
          t2v("Sorry The Database"+dbname+" does not exist.please Enter an existing Database name")
      else:
          dropdb(dbname)
          print("Database ",dbname," has been Deleted Successfully")
          t2v("Database "+dbname+" has been Deleted Successfully")
          listdb=alldbs()
          for i in listdb:
             print(i)
             
  #end of drop database
  #alter table

  elif(("alter" in command and "table" in command) or ("change" in command and "schema" in command)):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
          
        print("Enter the Table Name:")
        t2v("Enter the Table Name")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            altertb(tbname)
            print("Table has been ALtered Successfully")
            t2v("Table has been ALtered Successfully")
            
  #end of alter table
  #rename table

  elif("rename" in command and "table" in command):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("Enter the Table Name to rename:")
        t2v("Enter the Table Name to rename")
        tbname=input()
        print("Enter the new Table Name:")
        t2v("Enter the new Table Name")
        newtbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        elif newtbname in listtb:
            print("Sorry The Table ",newtbname," already exists.please Enter a existing table name")
            t2v("Sorry The Table "+newtbname+" already exists.please Enter a existing table name")
        else:
            renametb(tbname,newtbname)
            print("Table ",tbnamw," has been renamed as ",newtbname)
            t2v("Table "+tbnamw+" has been renamed as "+newtbname)
            
  #end of rename table
  #show databases

             
  elif (("show" in command or "select" in command) and "database" in command):
      listdb=alldbs()
      for i in listdb:
              print(i)

  #end of show databases
  #create table

  elif "create" in command and "table" in command:
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("Enter the Table Name:")
        t2v("Enter the Table Name")
        tbname=input()
        listtb=alltb()
        if tbname in listtb:
            print("Sorry The Table ",tbname," already exists.please Enter a different name")
            t2v("Sorry The Table "+tbname+" already exists.please Enter a different name")
        else:
            createtb(tbname)
            print("Table ",tbname," has been Created Successfully")
            t2v("Table "+tbname+" has been Created Successfully")
            listtb=alltb()
            for i in listtb:
                print(i)

  #end of create table
  #drop table

  elif ("drop" in command or "delete" in command) and "table" in command:
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("Enter the Table Name:")
        t2v("Enter the Table Name")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            droptb(tbname)
            print("Table ",tbname," has been deleted successfully")
            t2v("Table "+tbname+" has been deleted successfully")

  #end of drop table
  #truncate table

  elif(("truncate" in command and "table" in command) or ("remove all" in command and "table" in command) or ("free up" in command and "data" in command)):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("Enter the Table Name:")
        t2v("Enter the Table Name")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            truncatetb(tbname)
            print("The Table ",tbname," has been Truncated")
            t2v("The Table "+tbname+" has been Truncated")


  #end of truncate table
  #describe table

  elif ("desc" in command or "details" in command) and "table" in command:
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:")
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            tb("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            desctb(tbname)

  #end of describe table
  #show tables

  elif ("show" in command or "display" in command and "table" in command):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
          listtb=alltb()
          for i in listtb:
             print(i)

  #end of show tables
  #insert record

  elif (("insert" in command or "add record" in command or "new record" in command)and "table" in command):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("In which Table you want to insert?:")
        t2v("In which Table you want to insert?")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            insertrec(tbname)
            print("The given record has been inserted successfully")
            t2v("The given record has been inserted successfully")

  #end of insert record
  #update record

  elif (("update" in command or "update record" in command or "update entry" in command)and "table" in command):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("In which Table you want to update?:")
        t2v("In which Table you want to update?")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            updaterec(tbname)
            print("The Table has been updated successfully")
            t2v("The Table has been updated successfully")
            
            
  #end of update record
  #delete record

          
  elif(("delete" in command or "remove record" in command or "remove entry" in command) and "table" in command):
      if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
      else:
        print("In which Table you want to delete record?:")
        t2v("In which Table you want to delete record?")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            delterec(tbname)
            print("The record(s) has been deleted successfully")
            t2v("The record(s) has been deleted successfully")
                

  #end of delete record
  #select record

  elif(("select from" in command or "select" in command or "*" in command or "show record" in command or "select all" in command or "display record" in command or "display all" in command) and "table" in command):
     if dbname==None:
          print("Please select a database first")
          t2v("Please select a database first")
     else:
        print("Which Table record you want to display?:")
        t2v("Which Table record you want to display?")
        tbname=input()
        listtb=alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
            t2v("Sorry The Table "+tbname+" does not exist.please Enter a existing table name")
        else:
            print("Do you want to display all the records in Table?:")
            t2v("Do you want to display all the records in Table?")
            selallrec=input().lower()
            print("Do you want to display all the Fields in Table?:")
            t2v("Do you want to display all the Fields in Table?")
            selallfield=input().lower()
            selectrec(tbname,selallrec,selallfield)
            
 
  #end of select record
  #commit
  elif ("commit" in command):
    commit()
    print("Committed Seuccessfully")
    t2v("Committed Seuccessfully")

  #end of commit


  print("Enter The SQL command\n")
  command=v2t()
  print(command)

else:
  exit()
