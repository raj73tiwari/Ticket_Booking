<script setup>
import { ref, onMounted, watch } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import { useRouter } from "vue-router"
import TheatreForm from '../components/TheatreForm.vue';
import ShowForm from '../components/ShowForm.vue';
import ShowCardAdmin from '../components/ShowCardAdmin.vue';
import ShowCardPlaceholder from '../components/ShowCardPlaceholder.vue'

const router = useRouter()
const toast = useToast();

const theatres = ref(null)
const users = ref(null)
const shows = ref(null)

const getTheatre = async () => {
  try {
    const response = await axios.get('/theatre')
    theatres.value = response.data
    console.log(response.data)
  }
  catch (error) {

    toast.error("Server Error !")
    if (error.response) {
      console.log(error.response)

    }
  }

}
const getUser = async () => {
  try {
    const response = await axios.get('/user')
    users.value = response.data
    console.log(response.data)
  }
  catch (error) {

    toast.error("Server Error !")
    if (error.response) {
      console.log(error.response)
    }
  }

}
const getShow = async () => {
  try {
    const response = await axios.get('/show')
    shows.value = response.data
    showShow.value = response.data
    console.log(response.data)
  }
  catch (error) {

    toast.error("Server Error !")
    if (error.response) {
      console.log(error.response)
    }
  }

}



const showShow = ref([])
const searched = ref("")
watch(searched, () => {
  console.log(searched)
  showShow.value = shows.value.filter(s => s.name.toLowerCase().includes(searched.value.toLowerCase()) || s.tags.toLowerCase().includes(searched.value.toLowerCase()))
})

onMounted(() => {
  getTheatre()
  getUser()
  getShow()
});

const handleSForm = async (val) => {
  s_form.value = !s_form.value
  if (val) {
    await getShow()
  }

}
const handleTForm = async (val) => {
  t_form.value = t_form.value
  if (val) {
    await getTheatre()
  }

}
const t_list = ref(false)
const s_list = ref(true)
const u_list = ref(false)

const t_form = ref(false)
const s_form = ref(false)


</script>



<template>
  <div class="view">
    <TheatreForm @closed="handleTForm" v-if="t_form" />
    <ShowForm @closed="handleSForm" v-if="s_form" />

    <h1 class="text-center pt-3 ">Admin Panel</h1>
    <div class="row">
      <div class="col-4">
        <div class="info" @click=" t_list = true, u_list = false, s_list = false">
          <h4>Total Theatres</h4>
          <p><i class="bi bi-building-fill me-2" style="color: rgb(228, 210, 47);"></i>{{ theatres ? theatres.length : "..."
          }}</p>
        </div>
        <button type="button" class="btn btn-primary " @click="t_form = !t_form"><i
            class="bi bi-plus-circle me-2"></i>Theatre</button>
      </div>
      <div class="col-4">
        <div class="info" @click="s_list = true, t_list = false, u_list = false">
          <h4>Total Shows</h4>
          <p><i class="bi bi-film me-3" style="color: #35b389; font-size: 35px;"></i>{{ shows ? shows.length : "..." }}</p>
        </div>
        <button type="button" class="btn btn-primary " @click="s_form = !s_form"><i
            class="bi bi-plus-circle me-2"></i>Show</button>
      </div>
      <div class="col-4" style="margin-top: -0.1rem;">
        <div class="info" @click="u_list = true, t_list = false, s_list = false">
          <h4>Total Users</h4>
          <p><i class="bi bi-people-fill me-3" style="color: #b33535;"></i>{{ users ? users.length : "..." }}</p>
        </div>
      </div>

    </div>
    <div class="list" v-if="t_list || u_list">
      <h2 class="text-center mb-4" v-if="t_list"> All Theatres</h2>
      <h2 class="text-center mb-4" v-if="u_list"> All Users</h2>
      <h2 class="text-center mb-4" v-if="s_list"> All Shows</h2>
      <table class="table table-dark table-striped">
        <thead>
          <tr v-if="t_list">
            <th scope="col" style="font-weight: 900;">ID</th>
            <th scope="col" style="font-weight: 900;">Name</th>
            <th scope="col" style="font-weight: 900;">Capacity</th>
            <th scope="col" style="font-weight: 900;">Address</th>
          </tr>
          <tr v-if="u_list">
            <th scope="col" style="font-weight: 900;">ID</th>
            <th scope="col" style="font-weight: 900;">User Name</th>
            <th scope="col" style="font-weight: 900;">Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="t_list" v-for="t in theatres">
            <td>{{ t.id }}</td>
            <td>{{ t.name }}</td>
            <td>{{ t.capacity }}</td>
            <td>{{ t.address }}</td>
          </tr>
          <tr v-if="u_list" v-for="u in users">
            <td>{{ u.id }}</td>
            <td>{{ u.user_name }}</td>
            <td>{{ u.email }}</td>

          </tr>
        </tbody>
      </table>

    </div>

    <div class="s_view" v-if="s_list">
      <Alert v-if="isDelete" @closed="handleDelete" />


      <div class="row">
        <div class="col-4">


        </div>
        <div class="col-4">


          <h2>All Shows</h2>
        </div>
        <div class="col-4">
          <form class="d-flex" role="search">
            <input class="form-control me-2 ms-2" type="search" placeholder="Search..." aria-label="Search"
              v-model="searched">
          </form>
        </div>
      </div>

      <div class="contain">

        <h2 v-if="shows && showShow.length == 0">Sorry, no shows found !</h2>
        <ShowCardAdmin v-if="shows" v-for="s in showShow" :show="s" @changed="getShow" />
        <ShowCardPlaceholder v-else v-for="n in 6" />


      </div>
    </div>

  </div>
</template>
  
<style scoped>
h1 {
  font-family: 'Belanosima';
  letter-spacing: 2px;
  font-weight: bold;
  color: antiquewhite;
  margin-bottom: 0%;
}

.s_view {
  position: relative;
}



button.btn.btn-primary {
  background-color: #2d2747;
  border: 1px solid #2d2747;
  border-radius: 3px;
  color: bisque;
  font-weight: 500;
  padding: 5px 10px;

}

button.btn.btn-del {
  background-color: #ca1f1f;
  border: 1px solid #ca1f1f;
  border-radius: 3px;
  color: bisque;
  font-weight: 500;
  padding: 5px 10px;

}

.col-4 {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2%;
  margin: auto;
}

.row {
  margin: 0%;
}

::placeholder {
  color: antiquewhite;
  opacity: 0.5;
}

input {
  background-color: #202124;
  border: 1px solid #50544E;
  color: aliceblue;
  font-family: 'Patua One';
  letter-spacing: 1px;

}

input:focus {
  background-color: #202124;
  border-color: #50544E;
  box-shadow: 0px 0px 8px 3px rgb(33, 150, 243, 0.3);
  color: aliceblue;
}

.contain {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-top: 3%;
}

.view {
  position: relative;
  min-height: 100vh;
  margin-top: 0%;
}



button.btn.btn-primary {
  background-color: #1b5c56;
  border: 1px solid #1b5c56;
  border-radius: 3px;
  color: bisque;
  font-weight: 500;
  padding: 5px 10px;

}

.col-4 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4%;
  margin: auto;
}


.row {
  margin: 0%;
}

.info {
  padding: 12%;
  margin: 10%;
  background-color: #2d2747;
  min-height: 150px;
  width: 100%;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  cursor: pointer;
  transition: all .3s ease-in-out;


}

.info:hover {
  transform: translate3d(0px, -2px, 0px);
}

p {
  font-size: 40px;
  margin-bottom: 0%;
  color: #aeda84;
}

h4 {
  margin-bottom: 0%;
  color: bisque;
}

h2 {
  color: rgb(118, 150, 139);
}

.list {
  max-width: 100vw;
  padding: 5%;
}</style>
  