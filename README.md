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
   
   <p>
    <img src="/images/API endpoints.png" width="100%" height="100%" />
   </p>
   
   ```
   1) /token : Given the username and password returns the acess token if the credentials are valid
   2) /signup: Given the username and password and fullname it creates an user account
   3) /users/me: Provides the information about logged in user
   4) /uploadfile: Given a file it uploads the file to the server which can only be accessed by the logged in user
   5) /sharefiles: Given a fileid and the username the file gets shared to the respective user
   6) /getfiles: It returns all the files that are accessible by the logged in user
   7) /renamefile: Given a fileid and new name the respective file gets renamed
   8) /deletefile: Given a fileid the respective file will be deleted (The user can no longet access the file)
   9) /downloadfile: Given a fileid it returns the respective file as responce
   ```
   # Client application (CLI)
   
   - I have developed a CLI application for client side using python, with the help of the CLI the user can:
     <br>      *1)signup, login*
     <br>      *2) upload files*
     <br>      *3) view the files that he has uploaded and the files shared with him*
     <br>      *4) download files*
     <br>      *5) share the files*
     <br>      *6)rename the files*
     <br>      *7)delete the files*
