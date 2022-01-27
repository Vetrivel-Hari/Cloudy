let app = new Vue({
    el: "#app",
    
    data: {
        username: "",
        fullname: "",
        password: "",
        rePassword: "",
    },

    methods: {
        createAccount: function()
        {
            if(isValidUsername(this.username))
            {
                if(isValidFullname(this.fullname))
                {
                    if(isValidPassword(this.password))
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
                                    alert("Username already registered")
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
                            alert("BOTH THE PASSWORDS SHOULD MATCH")
                        }
                    }
                    else
                    {
                        alert("PASSWORD SHOULD HAVE ATLEAST 8 characters and 1 capital letter")
                    }
                }
                else
                {
                    alert("INVALID FULLNAME")
                }
            }
            else
            {
                alert("USERNAME SHOULD BE IN LOWERCASE AND ATLEAST 5 characters long. Only LETTERS are allowed!")
            }

        }

    }
})

function isValidUsername(s)
{
    rx = /^([a-z]+$)/

    if(s.length >= 5)
    {
        if(rx.test(s) == true)
            return true
        else
            return false
    }
    else
        return false
}

function isValidFullname(s)
{   
    rx = /^([a-zA-Z]+$)/

    if(s.length >= 0)
    {
        if(rx.test(s) == true)
            return true
        else
            return false
    }
    else
        return false
}

function isValidPassword(s)
{
    if(s.length >= 8)
    {
        for(let i=0; i<s.length; i++)
        {
            if("ABCDEFGHIJKLMNOPQRSTUVWXYZ".includes(s[i]))
                return true
        }

        return false
    }
    else
        return false
}
