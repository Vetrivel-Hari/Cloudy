//Function to get a cookie by name
const getCookie = (cookie_name) =>{
    // Construct a RegExp object as to include the variable name
    const re = new RegExp(`(?<=${cookie_name}=)[^;]*`);
    try{
      return document.cookie.match(re)[0];	// Will raise TypeError if cookie is not found
    }catch{
      return "this-cookie-doesn't-exist";
    }
  }

  let app = new Vue({
      el: "#app",
      data: {
           access_token: "",
           username: "",
           uploadWarning: ""
      },
      
      created()
      {
          this.access_token = getCookie("access_token")
          let s = 'Bearer ' + this.access_token
          fetch('http://127.0.0.1:8000/users/me',
          {
              headers:
              {
                'Content-Type' : 'application/json',
                'Authorization' : s
              }
          })
          .then((responce) => {
            if(responce.status == 400)
            {
                window.location.replace('http://127.0.0.1:5000/')
                throw 'INACTIVE USER'
            }
            else
                return responce.json()
            
          })
          .then((data) => {
                this.uploadWarning = ""
          })
          .catch((error) => {
              console.log(error)
          })
        },
        
        methods:{
          fileUpload: function() {
              form = new FormData(document.getElementById("form-upload"))
              this.access_token = getCookie("access_token")
              let s = 'Bearer ' + this.access_token
              
              console.log(s)
              
              fetch('http://127.0.0.1:8000/uploadfile',
              {
                method: 'POST',
                headers:
                {
                  'accept' : 'application/json',
                  'Authorization' : s,
                  'Content-Type': 'multipart/form-data'
                },
                body: form
              })
              .then((responce) => {
                if(responce.status == 400)
                {
                  console.log(responce)
                  this.uploadWarning = "FILE ALREADY EXISTS IN THE CLOUD"
                  throw 'FILE ALREADY EXISTS IN THE CLOUD'
                }
                else
                  return responce.json()   
                })
                .then((data) => {
                  this.uploadWarning = data.filename
                  alert("FILE UPLOADED SUCCESSFULLY")
                })
                .catch((error) => {
                    console.error('Error: ', error)
                })
          }
        }
  })