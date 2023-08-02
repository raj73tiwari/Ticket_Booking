<script setup>
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';
import TheatreCard from '../components/TheatreCard.vue';
import TheatrePlaceholder from '../components/TheatrePlaceholder.vue';
import TheatreForm from '../components/TheatreForm.vue';
import { useUserStore } from '../stores/users';
import { useToast } from 'vue-toastification';
const toast = useToast();

const userStore = useUserStore()

const getTheatre = async () => {
  try {
    const response = await axios.get('/theatre')
    theatres.value = response.data
    showTheatre.value = response.data
  }
  catch (error) {
    
      toast.error("Server Error !")
      if (error.response) {
        console.log(error.response)
      
    }
  }

}

onMounted(
  getTheatre
)

const handleForm = async (val) => {
  isForm.value = !isForm.value
  if(val){
    await getTheatre()
  }
  
}

const theatres = ref(null)
const showTheatre = ref([])
const searched = ref("")
const isForm = ref(false)
watch(searched, () => {
  showTheatre.value = theatres.value.filter(t => t.name.toLowerCase().includes(searched.value.toLowerCase()) || t.address.toLowerCase().includes(searched.value.toLowerCase()))
})





</script>

<template>
  <div class="view">
      <TheatreForm @closed=handleForm v-if="isForm"/>
    <div class="row">
      <div class="col-4">
        <button type="button" v-if="userStore.isAdmin()" class="btn btn-primary" @click="isForm = !isForm"><i
            class="bi bi-plus-circle me-2"></i>Theatre</button>
      </div>
      <div class="col-4">


        <h1>Theatres</h1>
      </div>
      <div class="col-4">
        <form class="d-flex" role="search">
          <input class="form-control me-2 ms-2" type="search" placeholder="Search..." aria-label="Search"
            v-model="searched">
        </form>
      </div>
    </div>
    <div class="container">
      <h2 v-if="theatres && showTheatre.length == 0">Sorry, no theatres found !</h2>
      <TheatreCard v-if="theatres" v-for="theat in showTheatre" :name=theat.name :img=theat.image_name
        :seat=theat.capacity :id=theat.id :address=theat.address />
      <TheatrePlaceholder v-else v-for="n in 6" />
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Belanosima|Patua+One|Pacifico');

h1 {
  font-family: 'Belanosima';
  letter-spacing: 2px;
  font-weight: bold;
  color: antiquewhite;
  margin-bottom: 0%;
}

.view {
  position: relative;
  min-height: 100vh;
}



button.btn.btn-primary {
  background-color: #2d2747;
  border: 1px solid #2d2747;
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


.container {
  padding: 1%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  min-height: 50vh;

}
</style>