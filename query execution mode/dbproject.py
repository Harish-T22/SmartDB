import dboperations as db
dbname= None
db.enableautocommit()
command=input("Enter The SQL command\n").lower()
while(command != "exit" and command != "quit" and command != "bye"):
  
  #create database
  
  if "create" in command and "database" in command:
      dbname=input("Enter the Database Name:\n")
      listdb=db.alldbs()
      if dbname in listdb:
          print("Sorry The Database",dbname," already exists.please Enter a different name")
      else:
          db.createdb(dbname)
          print("Database ",dbname," has been Created Successfully and you are currently using it")
          db.connect_db(dbname)
          listdb=db.alldbs()
          for i in listdb:
              print(i)
              
  #end of create database
  #use database
              
  elif (("select" in command or "use" in command) and "database" in command):
      dbname=input("Enter the Database Name:\n")
      listdb=db.alldbs()
      if dbname not in listdb:
          print("Sorry The Database",dbname," does not exist.please Enter an existing Database name")
      else:
          db.usedb(dbname)
          print("Databse ",dbname," has been selected")
          
  #end of use database
  #drop database
          
  elif (("delete" in command or "drop" in command) and "database" in command):
      dbname=input("Enter the Database Name:\n")
      listdb=db.alldbs()
      if dbname not in listdb:
          print("Sorry The Database",dbname," does not exist.please Enter an existing Database name")
      else:
          db.dropdb(dbname)
          print("Database ",dbname," has been Deleted Successfully")
          listdb=db.alldbs()
          for i in listdb:
             print(i)
             
  #end of drop database
  #alter table

  elif(("alter" in command and "table" in command) or ("change" in command and "schema" in command)):
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.altertb(tbname)
            print("Table has been ALtered Successfully")
            
  #end of alter table
  #rename table

  elif("rename" in command and "table" in command):
      if dbname==None:
          print("Please select a database first")
      else:  
        tbname=input("Enter the Table Name to rename:")
        newtbname=input("Enter the new Table Name:")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        elif newtbname in listtb:
            print("Sorry The Table ",newtbname," already exists.please Enter a existing table name")
        else:
            db.renametb(tbname,newtbname)
            print("Table "+tbnamw+"has been renamed as "+newtbname)
            
  #end of rename table
  #show databases

             
  elif (("show" in command or "select" in command) and "database" in command):
      listdb=db.alldbs()
      for i in listdb:
              print(i)

  #end of show databases
  #create table

  elif "create" in command and "table" in command:
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:\n")
        listtb=db.alltb()
        if tbname in listtb:
            print("Sorry The Table ",tbname," already exists.please Enter a different name")
        else:
            db.createtb(tbname)
            print("Table ",tbname," has been Created Successfully")
            listtb=db.alltb()
            for i in listtb:
                print(i)

  #end of create table
  #drop table

  elif ("drop" in command or "delete" in command) and "table" in command:
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.droptb(tbname)
            print("Table "+tbname+" has been deleted successfully")

  #end of drop table
  #truncate table

  elif(("truncate" in command and "table" in command) or ("remove all" in command and "table" in command) or ("free up" in command and "data" in command)):
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.truncatetb(tbname)
            print("The Table "+tbname+" has been Truncated")


  #end of truncate table
  #describe table

  elif ("desc" in command or "details" in command) and "table" in command:
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("Enter the Table Name:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.desctb(tbname)

  #end of describe table
  #show tables

  elif ("show" in command or "display" in command and "table" in command):
      if dbname==None:
          print("Please select a database first")
      else:
          listtb=db.alltb()
          for i in listtb:
             print(i)

  #end of show tables
  #insert record

  elif (("insert" in command or "add record" in command or "new record" in command)and "table" in command):
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("In which Table you want to insert?:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.insertrec(tbname)
            print("The given record has been inserted successfully")

  #end of insert record
  #update record

  elif (("update" in command or "update record" in command or "update entry" in command)and "table" in command):
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("In which Table you want to update?:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.updaterec(tbname)
            print("The Table has been updated successfully")
            
            
  #end of update record
  #delete record

          
  elif(("delete" in command or "remove record" in command or "remove entry" in command) and "table" in command):
      if dbname==None:
          print("Please select a database first")
      else:
          
        tbname=input("In which Table you want to delete record?:\n")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            db.delterec(tbname)
            print("The record(s) has been deleted successfully")
                

  #end of delete record
  #select record

  elif(("select from" in command or "select" in command or "*" in command or "show record" in command or "select all" in command or "display record" in command or "display all" in command) and "table" in command):
     if dbname==None:
          print("Please select a database first")
     else:
        
        tbname=input("Which Table record you want to display?:")
        listtb=db.alltb()
        if tbname not in listtb:
            print("Sorry The Table ",tbname," does not exist.please Enter a existing table name")
        else:
            selallrec=input("Do you want to display all the records in Table?:").lower()
            selallfield=input("Do you want to display all the Fields in Table?:").lower()
            db.selectrec(tbname,selallrec,selallfield)
            
 
  #end of select record
  #commit
  elif ("commit" in command):
    db.commit()
    print("Committed Seuccessfully")

  #end of commit


  command=input("Enter The SQL command\n").lower()

else:
  exit()
