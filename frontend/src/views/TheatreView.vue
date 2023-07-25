<script setup>

import axios from 'axios';
import ShowCard from '../components/ShowCard.vue';
import { useRoute } from 'vue-router';
import { onMounted ,ref} from 'vue';
import Alert from '../components/Alert.vue';
import {useRouter} from "vue-router"
import { useToast } from 'vue-toastification';
import TheatreForm from '../components/TheatreForm.vue';
const toast = useToast();

const router=useRouter()
const route = useRoute()

const name=ref('')
const curr_theat=ref(null)
const isDelete=ref(false)
const isUpdate=ref(false)

const getTheatre = async () => {
  try {
    const response = await axios.get(`/getTheatre/${parseInt(route.params.id)}`)
    curr_theat.value = response.data
    name.value=response.data.name
  }
  catch (error) {
    if (error.response && error.response.status === 404)  {

      toast.error(error.response.data.message)

    }
    else {
      toast.error("Server Error !")
      if (error.response) {
        console.log(error.response)
      }
    }
  }

}

onMounted(
  getTheatre
)
const handleUpdate = async (val) => {
  isUpdate.value = !isUpdate.value
  if(val){
    await getTheatre()
  }
  
}

const handleDelete=async(val)=>{
  isDelete.value=!isDelete.value
  if(val){
    try {
    const response = await axios.post(`/deleteTheatre/${parseInt(route.params.id)}`)
    router.replace('/')
    toast.success(response.data.message)
  }
  catch (error) {
    if (error.response && error.response.status === 404)  {

      toast.error(error.response.data.message)

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
</script>

<template>
<div class="view">
  <Alert v-if="isDelete" @closed="handleDelete"/>
  <TheatreForm v-if="isUpdate" :theatre="curr_theat" @closed="handleUpdate"/>

    <div class="row">
      <div class="col-4">
        <button type="button" class="btn btn-primary me-5 " @click="isUpdate=!isUpdate"><i class="bi bi-arrow-up-circle me-2"></i>Update</button>
        <button type="button" class="btn btn-del" @click="isDelete=!isDelete"><i class="bi bi-trash"></i></button>
      </div>
      <div class="col-4">


        <h1>{{ name}}</h1>
      </div>
      <div class="col-4">
        <form class="d-flex" role="search">
          <input class="form-control me-2 ms-2" type="search" placeholder="Search..." aria-label="Search"
            v-model="searched">
        </form>
      </div>
    </div>
 
  <div class="contain">
  <ShowCard/>
  <ShowCard/>
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
.view{
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
.contain{
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-top: 3%;
}
</style>