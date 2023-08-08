<script setup>

import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import { useUserStore } from '../stores/users';
import { useRoute } from "vue-router"


const toast = useToast();
const userStore = useUserStore()
const route = useRoute()

const props = defineProps(['show', 'seat'])
const emit = defineEmits(['changed'])


function getImageUrl(imageFilename) {
  return `http://localhost:5000/uploads/${imageFilename}`;
}

const handleRemove = async () => {

  try {
    const response = await axios.post(`/removeShow/${parseInt(route.params.id)}/${parseInt(props.show.id)}`)
    emit('changed')
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
const getSeats = async () => {

  try {
    const response = await axios.get(`/theatre/${parseInt(route.params.id)}/show/${parseInt(props.show.id)}/schedule/${parseInt(props.show.schedule_id)}/seats`)
    seats.value = response.data

  }
  catch (error) {
    if (error.response && error.response.status === 404) {

      console.log(error.response)

    }
    else {
      toast.error("Server Error !")
      if (error.response) {
        console.log(error.response)
      }
    }


  }
}
const handleBooking = async () => {

  try {
    const response = await axios.post(`/bookShow/${parseInt(route.params.id)}`, {
      user_id: userStore.user.id,
      show_id: props.show.id,
      schedule_id: props.show.schedule_id,

    })
    toast.success(response.data.message)
    booked.value = true
    await getSeats()
  }
  catch (error) {
    if (error.response && (error.response.status === 404 || error.response.status == 400)) {

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

const booked = ref(false)
const seats = ref(null)

onMounted(
  getSeats
)




</script>


<template>
  <div class="show-card dark-theme">

    <div class="show-image">
      <img :src="getImageUrl(show.image_name)" alt="Show Image" />
    </div>
    <div class="contain">
      <div class="row">
        <div class="col-8">
          <div class="show-details">
            <div class="show-header">
              <h1 class="show-name">{{ show.name }}</h1>
            </div>
            <div class="show-info">
              <div class="show-row">
                <p class="show-price">
                  <i class="bi bi-currency-dollar icon" style="color: rgb(144, 192, 72);"></i>
                  {{ show.price }}
                </p>
                <p class="show-tickets">
                  <i class="bi bi-ticket icon" style="color: rgb(228, 167, 88);"></i>
                  {{ seats }}
                </p>
                <p class="show-rating">
                  <i class="bi bi-star icon " style="color: rgb(194, 194, 48);"></i>
                  {{ show.rating }}
                </p>
              </div>
            </div>
            <div class="show-tags">
              <span v-for="tag in show.tags.split(',')" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="show-action">
            <button v-if="userStore.isAdmin()" class="book-button" style="background-color: rgb(196, 66, 66);"
              @click=handleRemove>
              <i class="bi bi-x me-2"></i>
              Remove
            </button>
            <button v-else class="book-button" @click="handleBooking">
              <!-- <i v-if="booked" class="bi bi-bookmark-check me-1" style="color: #639138; font-size: 15px;"></i> -->
              <i class="bi bi-bookmark me-1"></i>
              Book
            </button>
            <p class="show-time" style="font-size: 15px; margin-left: -20px;">
              <i class="bi bi-clock icon" style="  color: #f08ace; font-size: 15px;"></i>
              {{ show.time }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<style >
.show-action {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-top: 35px;
}

.conatin {
  display: flex;
  justify-content: center;
}

.show-card {
  display: grid;
  grid-template-columns: 1fr 2fr;
  background-color: #0d1929;
  color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 16px;
  width: 90%;
  margin-bottom: 3%;
}

.show-image {
  max-width: 80%;
  overflow: hidden;
  border-radius: 8px;
  height: 180px;
}

.show-image img {
  width: 100%;
  height: 100%;
}

.show-details {
  flex: 1;

}

.show-name {
  font-size: 30px;
  margin: 0;
  margin-bottom: 8px;
  margin-top: 8px;
}

.book-button {
  background-color: #28a745;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: bold;
  margin-bottom: 20px;
  width: 130px;
}

.booked-button {
  background-color: #27382e;
  color: #5c8b5a;
}

.show-info {
  margin-bottom: 5px;
  margin-top: 20px;
}

.show-row {
  display: flex;
  align-items: center;
  margin-right: 16px;
}

.show-row p {
  margin-right: 24px;
}

.show-info .icon {
  margin-right: 8px;
  color: #61dafb;
  font-size: 1.2rem;
}

.show-time {
  font-size: 18px;
  padding-top: 4px;
  color: bisque
}

.show-tags {
  display: flex;
  flex-wrap: wrap;
  margin-top: 20px;
}

.tag {
  background-color: #417d9a;
  color: #ffffff;
  padding: 5px 10px;
  border-radius: 4px;
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>
  