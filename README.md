# Cloudy
## Cloudwiry Hackathon 2022

Problem Description: https://docs.google.com/document/d/11e6VnFdfBYa1i6SA8CIAuIFCzcWZGlDLyJSmYBf2AKQ/edit#heading=h.dn8jjv96h6n9

# User Authentication:
   
   - I have implemented ***OAuth 2.0*** for User Authentication with the help of FASTAPI. Whenever the user tries to login he should provide his username and password. If the credentials given by the user is valid then the server will return a signed access token to the user. 
   - For all further requests to the API endpoints the user should attach the access token in the request header. 
   - As the access token in signed even if the user tries to manipulate the token the token will become invalid.

# Implementation of the Blob Storage Server

   - I have used FASTAPI to develop the backend for this application
   - The API has various endpoints:
   
   <img src="/images/API endpoints.png" width="100%" height="100%" />
   
   
   ```
   1) /token : Given the username and password returns the acess token if the credentials are valid
   2) /signup: Given the username and password and fullname it creates an user account
   3) /users/me: Provides the information about logged in user
   4) /uploadfile: Given a file it uploads the file to the server which can only be accessed by the logged in user
   5) /sharefiles: Given a fileid and the username the file gets shared to the respective user
   6) /getfiles: It returns all the files that are accessible by the logged in user
   7) /renamefile: Given a fileid and new name the respective file gets renamed
   8) /deletefile: Given a fileid the respective file will be deleted (The user can no longer access the file)
   9) /downloadfile: Given a fileid it returns the respective file as responce
   ```
   # Client application (CLI)
   
   - I have developed a CLI application for client side using python, with the help of the CLI the user can:
     <br>      *1) signup, login*
     <br>      *2) upload files*
     <br>      *3) view the files that he has uploaded and the files shared with him*
     <br>      *4) download files*
     <br>      *5) share the files*
     <br>      *6) rename the files*
     <br>      *7) delete the files*
     <br>
   - I have used ***requests*** module available in python to send requests to the API endpoints and manipulate the responce received from the server
   - Checkout the Demo Video: [Click to view the video](https://www.google.com/)
     
   # Database
   
   - I have used PostgreSQL for database
   
   <img src="/images/ERD.png" width="100%" height="100%" />
  
   - The above image is the ERD diagram for the database that I have created and used
   - The files that the user uploads will be stored in the ***userFiles directory*** present in the server
   - Inside the ***userFiles directory*** each user has his own ***individual directory***
   
   ### Sharing the files don't maintain a duplicate copy in the server. I have taken inspiration from the concept of ***hard-links*** in linux to implement the sharing functionality. 
   
   # How to run the application?
   
   - You need to create the database, Copy the sql commands from the file ***SQLQuery.txt*** and execute it in PostgreSQL
      <br> Note: In /sql_app/database.py you need to change the value of the variable ***SQLALCHEMY_DATABASE_URL*** to point to your database
   
   - Open the terminal and install the required modules mentioned in the ***requirments.txt*** file.
   
   > pip install -r requirments.txt
  
   - Locate the folder ***Cloudy*** using the command line and run the command ***uvicorn main:app*** to start the server
     <br> Note: main.py file contains the backend code (code for the API)
          
   - Open a new Terminal, Locate the folder ***Cloudy*** using the command line and run the command ***python app.py*** to start the CLI application
     <br> Note: app.py file contains the code for CLI application
     <br> You can interact with the API using this CLI application
     
   # Reference
   
   - FASTAPI: [Documentation](https://fastapi.tiangolo.com/)

   <hr />
