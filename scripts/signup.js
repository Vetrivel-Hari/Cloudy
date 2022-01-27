let app = new Vue({
    el: "#app",
    
    data: {
        username: "",
        fullname: "",
        password: "",
        rePassword: "",

        usernameWarning: "",
        fullnameWarning: "",
        passwordWarning: "",
        repasswordWarning: "",
    },

    methods: {
        createAccount: function()
        {
            //Check the constraints
            if(isValidUsername())
            {
                if(isValidFullname())
                {
                    if(isValidPassword())
                    {
                        if(this.password === this.rePassword)
                        {
                            data = {"username" : this.username,
                                    "fullname" : this.fullname,
                                    "password" : this.password }

                            fetch('http://127.0.0.1:8000/signup',
                            {
                                method: 'POST',
                                headers: {
                                    'Content-Type' : 'application/json'
                                },
                                body: JSON.stringify(data)
                            })
                            .then((response) => {
                                if(response.status == 400)
                                {
                                    this.usernameWarning = "Username already registered"
                                    throw 'Username already registered'
                                }
                                else
                                    return response.json
                            })
                            .then((data) => {
                                if(data)
                                alert("Account Created Successfully")

                            })
                            .catch((error) => {
                                console.error('Error: ', error)
                            })

                        }
                        else
                        {
                            this.repasswordWarning = "BOTH THE PASSWORDS SHOULD MATCH"
                        }
                    }
                    else
                    {
                        this.repasswordWarning = "PASSWORD SHOULD HAVE ATLEAST 8 characters and 1 capital letter"
                    }
                }
                else
                {
                    this.fullnameWarning = "INVALID FULLNAME"
                }
            }
            else
            {
                this.usernameWarning = "USERNAME SHOULD BE IN LOWERCASE AND ATLEAST 5 characters long"
            }

        }

    }
})

function isValidUsername()
{
    return true
}

function isValidFullname()
{
    return true
}

function isValidPassword()
{
    return true
}