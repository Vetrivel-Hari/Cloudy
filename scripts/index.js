let access_token = ""

let app = new Vue({
    el: "#app",
    
    data: {
        username: "",
        password: "",

        usernameWarning: "",
    },

    methods: {
        checkCredentials: function()
        {
            if((this.username.length >=5) && (this.password.length >=8))
            {
                form = new FormData(document.getElementById("form-login"))
                fetch('http://127.0.0.1:8000/token',
                {
                    method: 'POST',
                    body: form
                })
                .then((responce) => {
                    if(responce.status == 401)
                    {
                        this.usernameWarning = "INVALID USERNAME or PASSWORD"
                        throw 'INVALID USERNAME or PASSWORD'
                    }
                    else
                        return responce.json()
                    
                })
                .then((data) => {
                    let c = "access_token=" + data.access_token
                    document.cookie=c

                    window.location.replace('http://127.0.0.1:5000/templates/homepage.html')
                    alert("LOGIN SUCCESS")
                })
                .catch((error) => {
                    console.error('Error: ', error)
                })
            }
            else
                this.usernameWarning = "INVALID USERNAME or PASSWORD"

        }

    }
})
