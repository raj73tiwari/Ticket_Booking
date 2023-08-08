<script setup>

import axios from 'axios';
import ShowCard from '../components/ShowCard.vue';
import ShowCardPlaceholder from '../components/ShowCardPlaceholder.vue';
import { useRoute } from 'vue-router';
import { onMounted, ref, watch } from 'vue';
import Alert from '../components/Alert.vue';
import { useRouter } from "vue-router"
import { useToast } from 'vue-toastification';
import TheatreForm from '../components/TheatreForm.vue';
import AddShow from '../components/AddShow.vue';
import { useUserStore } from '../stores/users';

const userStore = useUserStore()
const toast = useToast();

const router = useRouter()
const route = useRoute()

const name = ref('')
const curr_theat = ref(null)
const isDelete = ref(false)
const isUpdate = ref(false)
const isAddShow = ref(false)




const shows = ref(null)
const showShows = ref([])
const searched = ref("")

watch(searched, () => {
  showShows.value = shows.value.filter(s => s.name.toLowerCase().includes(searched.value.toLowerCase()) || s.tags.toLowerCase().includes(searched.value.toLowerCase()))
})


const getShows = async () => {
  try {
    const response = await axios.get(`/getShows/${parseInt(route.params.id)}`)
    shows.value = response.data
    showShows.value = response.data
  }
  catch (error) {
    if (error.response && error.response.status === 404) {

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


const getTheatre = async () => {
  try {
    const response = await axios.get(`/getTheatre/${parseInt(route.params.id)}`)
    curr_theat.value = response.data
    name.value = response.data.name
  }
  catch (error) {
    if (error.response && error.response.status === 404) {

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

onMounted(() => {
  getTheatre()
  getShows()
});
const handleUpdate = async (val) => {
  isUpdate.value = !isUpdate.value
  if (val) {
    await getTheatre()
  }

}
const handleAddShow = async (val) => {
  isAddShow.value = !isAddShow.value
  if (val) {
    await getShows()
  }

}

const handleDelete = async (val) => {
  isDelete.value = !isDelete.value
  if (val) {
    try {
      const response = await axios.post(`/deleteTheatre/${parseInt(route.params.id)}`)
      router.replace('/')
      toast.success(response.data.message)
    }
    catch (error) {
      if (error.response && error.response.status === 404) {

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

const exporting = ref(false)

const exportData = async () => {
  if (exporting.value) return;
  try {
    exporting.value = true

    const response = await axios.post(`/export/${parseInt(route.params.id)}`);
    const resultId = response.data.result_id;
    await ExportResult(resultId, 5000, 1000);
    toast.success('Theatre data exported successfully');
  }
  catch (error) {
    if (error.response) {
      toast.error(error.response.data.message)

    }
    else {
      toast.error("Server Error !")
      if (error.response) {
        console.log(error.response)
      }
    }
  }
  finally {
    exporting.value = false
  }
};
async function ExportResult(resultId, timeout, interval) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    try {
      const response = await axios.get(`/export_result/${resultId}`);
      if (response.data.ready) {
        return;
      }
    } catch (error) {

    }
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  throw new Error('Export result polling timeout');
}

</script>

<template>
  <div class="view">
    <Alert v-if="isDelete" @closed="handleDelete" />
    <TheatreForm v-if="isUpdate" :theatre="curr_theat" @closed="handleUpdate" />
    <AddShow v-if="isAddShow" :t_id="curr_theat.id" @closed="handleAddShow" />

    <div class="row">
      <div class="col-4" v-if="userStore.isAdmin()">
        <button type="button" class="btn btn-primary me-3 " @click="isUpdate = !isUpdate"><i
            class="bi bi-arrow-up-circle me-2"></i>Update</button>
        <button type="button" class="btn btn-del me-3" @click="isDelete = !isDelete"><i class="bi bi-trash"></i></button>
        <button type="button" class="btn btn-primary me-5 "
          style="background-color: rgb(15, 128, 128); border-color: rgb(15, 128, 128)" @click="isAddShow = !isAddShow"><i
            class="bi bi-plus-circle me-2 "></i>Add Show</button>
      </div>
      <div class="col-4" v-else></div>
      <div class="col-4">


        <h1>{{ name }}</h1>
      </div>
      <div class="col-4">
        <form class="d-flex" role="search">
          <input class="form-control me-2 ms-2" type="search" placeholder="Search..." aria-label="Search"
            v-model="searched">
        </form>
        <button type="button" class="btn btn-export ms-3 " v-if="userStore.isAdmin()" @click="exportData"
          :disabled="exporting"><i class="bi bi-filetype-csv me-2"></i>Export</button>
      </div>
    </div>

    <div class="contain">

      <h2 v-if="shows && showShows.length == 0">Sorry, no shows found !</h2>
      <ShowCard v-if="shows" v-for="s in showShows" :show="s" :seat="curr_theat.capacity" @changed="getShows" />
      <ShowCardPlaceholder v-else v-for="n in 6" />
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

.view {
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

button.btn.btn-export {
  background-color: #7e6808;
  border: 1px solid #7e6808;
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
</style>