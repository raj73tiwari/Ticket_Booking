<script setup>

import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../stores/users';
import { useToast } from 'vue-toastification';
import { useRouter } from "vue-router"
const router = useRouter()

const toast = useToast();

const userStore = useUserStore()
const userName = ref('')
if (userStore.isUser()) {
  userName.value = userStore.user['user_name']
}
onMounted(() => {
  document.addEventListener('token-refresh-failed', handleTokenRefreshFailed);
});

const handleTokenRefreshFailed = async () => {
  toast.warning('Please Login Again !');
  await logout(false)
};

const logout = async (show) => {
  try {
    const response = await axios.post('logout')
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    userStore.removeUser()
    router.push('/')
    if (show) {
      toast.success(response.data.message)
    }
  }
  catch (error) {
    if (error.response) {
      console.log(error.response)
    }
    else {
      toast.error('Error : Server Error !')
    }
  }

}

</script>

<template>
  <nav class="navbar navbar-expand-lg " data-bs-theme="dark" style="background-color: #021729;">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">Book It</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink active-class="active" class="nav-link " aria-current="page" to="/">
              <i class="bi bi-house-fill"></i>
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink v-if="userStore.isUser() && !userStore.isAdmin()" active-class="active" class="nav-link"
              to="/profile"><i class="bi bi-person-fill"></i></RouterLink>
          </li>


          <li class="nav-item">
            <RouterLink active-class="active" class="nav-link" to="/about"><i class="bi bi-info-lg"></i></RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink v-if="userStore.isAdmin()" active-class="active" class="nav-link" to="/admin"><i
                class="bi bi-shield-lock"></i></RouterLink>
          </li>


        </ul>
        <div class="nav-item dropdown" style="margin-left: 4%;">
          <button v-if="userStore.isUser()" class="btn btn-dark dropdown-toggle" data-bs-toggle="dropdown"
            aria-expanded="false" style="color:bisque; font-size: 20px; font-weight: 600;">
            <img src="../assets/img/zxc.jpg" width="44" height="44" class="rounded-circle me-1">
            {{ userName }}
          </button>
          <RouterLink v-else class="btn btn-dark" to="/signin" style="color: #2196F3; font-size: 20px; font-weight: 600;">
            <img src="../assets/img/zxc.jpg" width="44" height="44" class="rounded-circle me-1">
            Login
          </RouterLink>


          <ul class="dropdown-menu dropdown-menu-dark">
            <li>
              <RouterLink active-class="active" v-if="!userStore.isAdmin()" class="dropdown-item" to="/profile">My Profile
              </RouterLink>
            </li>
            <li><a class="dropdown-item" style="cursor: pointer;" @click="logout(true)">Logout <i
                  class="bi bi-box-arrow-right ms-2 mt-2" style="color: red;"></i></a></li>
          </ul>
        </div>


        <!-- <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search..." aria-label="Search">
        <button type="button" >&nbsp;Search&nbsp;</button>
        
      </form> -->
      </div>
    </div>
  </nav>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css?family=Belanosima|Patua+One');

input {
  background-color: #06121F;

}

input:focus {
  background-color: #06121F;
  border-color: #0E9B71;
  box-shadow: 0px 0px 8px 3px rgb(153, 153, 153, 0.3);
}



.btn {
  background-color: transparent;
  border-color: transparent;
}

/* a:hover {
  background-color: #404040;
} */

a.nav-link.active {
  border-radius: 0;
  border-bottom: 5px solid #2196f3;
  color: #2196f3;
}



a.nav-link:hover {
  color: #2196f3;
}


.navbar-toggler {
  border-radius: 1rem;
  /* ....background: linear-gradient(to left, #03B3E3 0%, #0E9B71 100%); */
  margin: 1%;
  background: linear-gradient(90deg, #0E9B71, transparent) #2196f3;
  color: #fff;
  text-decoration: none;
  transition: background-color 1s;
  border: none;

}

.navbar-toggler:hover {
  background-color: #3f51b5;
}

.navbar {
  padding: 0.25%;
}

form {
  margin-right: 3%
}

.navbar-brand {
  background: #03B3E3;
  background: linear-gradient(to left, #03B3E3 0%, #0E9B71 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: Patua One;
  font-size: 2.25rem;
  font-weight: bold;
  padding: 0;
  margin-left: 3%;
  margin-right: 17%;



}

.container-fluid .nav-link {
  font-family: Patua One;
  font-size: 25px;
  margin-right: 0.25rem;
  margin-left: 3%;
  text-decoration: none;
  border-radius: 10px;
  padding: 0;
  padding-bottom: 3px;
  padding-top: 3px;
  padding-left: 30px;
  padding-right: 30px;





}

.nav-item {
  border-radius: 10px;
  margin-right: 2%
}
</style>