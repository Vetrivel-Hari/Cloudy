# Cloudy
## Cloudwiry Hackathon 2022

Problem Description: https://docs.google.com/document/d/11e6VnFdfBYa1i6SA8CIAuIFCzcWZGlDLyJSmYBf2AKQ/edit#heading=h.dn8jjv96h6n9

# User Authentication:
                  I have implemented OAuth 2.0 for User Authentication with the help of FASTAPI. Whenever the user tries to login he should provide his username and password. If the credentials given by the user is valid then the server will return a signed access token to the user. For all further requests to the API endpoints the user should attach the access token in the request header. As the access token in signed even if the user tries to manipulate the token the token will become invalid.
