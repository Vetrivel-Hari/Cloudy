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
           username: ""
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
                this.username = data.uid
          })
          .catch((error) => {
              console.log(error)
          })
      }
  })