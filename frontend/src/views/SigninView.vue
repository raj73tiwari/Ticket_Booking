<script setup>
import { ref } from 'vue';
import axios from 'axios'
import { useRouter } from "vue-router"
import { useUserStore } from '../stores/users';
import { useToast } from 'vue-toastification';
const toast = useToast();

const userStore = useUserStore()





const router = useRouter()
const toHome = () => {
    router.replace('/')
}


const alert = ref(false)
const dismissalert = () => {
    alert.value = false
    alerts = []
}

let alerts = []



const SignUp = async () => {
    if (username.value.length < 4) {
        alerts.push('Username too short ! (required 4)')
        alert.value = true
        icUsername.value = false
    }
    if (username.value.includes(' ')) {
        alerts.push('Empty spaces not allowed in username!')
        alert.value = true
        icUsername.value = false
    }
    if (password.value.length < 4) {
        alerts.push('Password too short ! (required 4)')
        alert.value = true
        icPassword.value = false
    }
    if (password.value.includes(' ')) {
        alerts.push('Empty spaces not allowed in password!')
        alert.value = true
        icPassword.value = false
    }
    if (email.value.length < 8 || email.value.includes(' ') || !email.value.includes('@')) {
        alerts.push('Please enter a valid email address !')
        alert.value = true
        icEmail.value = false
    }
    if (alerts.length == 0) {
        try {
            const response = await axios.post('signup', {
                user_name: username.value,
                email: email.value,
                password: password.value
            })
            alert.value = true

            alerts.push(response.data.message);
            chkd.value = !chkd.value

        }
        catch (error) {
            if (error.response && error.response.status === 422) {
                alert.value = true
                alerts.push(error.response.data.message)

            }

            else {
                toast.error("Server Error !")
                if (error.response) {
                    console.log(error.response)
                }
            }
        }
    }
}


const login = async () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    if (username.value.trim() != '' && password.value.trim() != '') {


        try {
            const response = await axios.post('login', {
                user_name: username.value,
                password: password.value
            })
            // console.log(response.data.access_token);
            // console.log(response.data.refresh_token);
            userStore.setUser(response.data.user)
            localStorage.setItem('token', response.data.access_token)
            localStorage.setItem('refresh_token', response.data.refresh_token)

            toast.success(`Welcome ${response.data.user['user_name']}`)
            toHome()
        }
        catch (error) {
            if (error.response && error.response.status === 403) {
                alert.value = true
                alerts.push(error.response.data.message)

            }
            else {
                toast.error("Server Error !")
                if (error.response) {
                    console.log(error.response)
                }
            }
        }
    }
    else {
        alert.value = true
        alerts.push('Please enter valid Username/Password !')
    }

}






const username = ref('')
const email = ref('')
const password = ref('')

const icUsername = ref(true)
const icEmail = ref(true)
const icPassword = ref(true)

const chkd = ref(true)
</script>

<template>
    <div class="contain">
        <div class="main" id="main">
            <input type="checkbox" id="chk" v-model="chkd">
            <div class="signup">
                <label for="chk" class="sig">Sign Up</label>
                <div class="user-box  ">
                    <input type="text" title="Enter Username" id="username" required autocomplete="off" v-model="username"
                        :class="{ wrong: !icUsername }" @focus="icUsername = true">
                    <label id="usernameLabel">Username</label>
                    <img src="../assets/img/ilogo.svg" alt="Logo" class="logo-img" id="userIcon" />
                    <i></i>
                </div>
                <div class="user-box">
                    <input type="text" title="Enter email" id="email" required autocomplete="off" v-model="email"
                        :class="{ wrong: !icEmail }" @focus="icEmail = true">
                    <label id="emailLabel">Email</label>
                    <img src="../assets/img/ilogo.svg" alt="Logo" class="logo-img" id="emailIcon">
                </div>
                <div class="user-box">
                    <input type="password" title="Enter password" id="password" required autocomplete="off"
                        v-model="password" :class="{ wrong: !icPassword }" @focus="icPassword = true">
                    <label id="passwordLabel">Password</label>
                    <img src="../assets/img/ilogo.svg" alt="Logo" class="logo-img" id="passIcon">
                </div>

                <button @click="SignUp" id="button">Sign up</button>

            </div>

            <div class="login">

                <label for="chk" class="log">Login</label>



                <div class="user-box ">

                    <input type="text" title="Enter Username" id="username2" required v-model="username">

                    <label>Username</label>

                </div>

                <div class="user-box">

                    <input type="password" title="Enter password" id="password2" required v-model="password">

                    <label>Password</label>

                </div>
                <button @click="login" id="button2">Login</button>

            </div>

        </div>
        <div class="myalert" v-if="alert">

            <h3 class="text-center mb-3" style="font-weight: 900;">Alerts!</h3>

            <ul v-for="a in alerts">
                <li>{{ a }}</li>
            </ul>

            <button type="button" @click="dismissalert"> ok</button>
        </div>


    </div>
</template>


<style scoped>
* {
    font-family: 'Red Hat Mono', monospace;
    margin: 0px;
    padding: 0px;
}



.contain {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: url(../assets/img/frm-bkg.png);
    background-size: cover;
    background-position: center center;


}

.main {
    width: 320px;
    background-color: #00000033;
    height: 500px;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 5px 20px 50px #000;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -250px 0 0 -160px;
    backdrop-filter: blur(30px);


}

@media screen and (max-width: 320px) {
    .main {
        left: 160px;

    }
}

@media screen and (max-height: 500px) {
    .main {
        top: 250px;

    }
}

.colorDiv {
    color: #fff;
    position: fixed;
    width: 40px;
    height: 40px;
    top: 20px;
    left: 0px;
    background: #333;
    z-index: 1000;
    border-radius: 0px 10px 10px 0px;
}

.colorDiv input {
    display: none;
}

.colorDiv label {
    margin: 10px;
    display: inline-block;
    width: 20px;
    height: 20px;
    background: #077;
}

#chk {
    display: none;
}

.signup {
    position: relative;
    width: 100%;
    height: 100%;
}

.user-box {
    position: relative;
    width: 60%;
    margin: 0px auto;


}

.user-box .wrong {
    border-bottom: 1px solid red;
    background-image: linear-gradient(0deg, rgba(255, 0, 0, .3) 0%, rgba(0, 0, 0, 0) 30%);
}


button {
    width: 60%;
    height: 40px;
    margin: 10px auto;
    justify-content: center;
    display: block;
    color: #fff;
    background-color: #077;
    font-size: 1em;
    font-weight: bold;
    margin-top: 10px;
    outline: none;
    border: none;
    border-radius: 5px;
    transition: .2s ease-in;
    cursor: pointer;
}

button:hover {
    background: #066;
}

.myalert button:hover {
    background: rgb(150, 78, 78);
}

.myalert button {
    background-color: rgb(192, 121, 121);
    width: 20%;
    padding: 0%;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
    border: 2px solid;
    border-color: rgb(150, 78, 78);


}

.myalert {
    margin-top: 4rem;
    height: 17rem;
    width: 27rem;
    padding-top: 1rem;
    padding-left: 3rem;
    padding-right: 3rem;
    border-radius: 0.5rem;
    background-color: #EEEEEE;
    z-index: 10;
    color: rgb(150, 78, 78);
    position: relative;
    border: 1px solid;
    border-color: rgb(150, 78, 78);


}



.login {
    height: 470px;
    background: #eee;
    border-radius: 60% / 10%;
    transform: translateY(-180px);
    transition: .8s ease-in-out;


}

#chk:checked~.login {
    transform: translateY(-530px);
}

#chk:checked~.login label {
    transform: scale(1);
}

#chk:checked~.signup .sig {
    transform: scale(.6);
    margin-top: 10px;
}

.user-box label {
    position: absolute;
    top: 13px;
    left: 0px;
    font-size: 16px;
    color: #fff;
    pointer-events: none;
    transition: .5s;
}

.user-box .logo-img {
    filter: invert(100%) sepia(0%) saturate(7448%) hue-rotate(136deg) brightness(112%) contrast(112%);
    width: 15px;
    height: 15px;
    position: absolute;
    top: 13px;
    right: 0px;

}

.user-box .logo-img:hover {
    filter: invert(50%) sepia(0%) saturate(7448%) hue-rotate(136deg) brightness(112%) contrast(112%);
}

.user-box input {
    padding: 10px 0px;
    padding-right: 17px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    color: #fff;
    margin-bottom: 30px;
    border: none;
    border-bottom: 1px solid #fff;
    outline: none;
    background: transparent;

}

.user-box input:focus~label,
.user-box input:valid~label {
    top: -20px;
    left: 0;
    font-size: 12px;
    font-weight: bold;
}

label[for="chk"] {
    font-size: 2.3em;
    justify-content: center;
    display: flex;
    font-weight: bold;
    cursor: pointer;
    transition: .5s ease-in-out;
}

.sig {
    color: #fff;
    margin: 40px;
}

.log {
    margin: 80px;
}

.login label,
.login input {
    color: #077;
}

.login input {
    border-color: #077;
}
</style>