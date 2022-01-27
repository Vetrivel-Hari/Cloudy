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
           access_token: ""
      },
      
      created()
      {
          this.access_token = getCookie("access_token")
      }
  })