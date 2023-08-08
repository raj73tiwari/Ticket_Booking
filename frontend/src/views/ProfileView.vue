<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { useUserStore } from '../stores/users';
import MyBookingCard from '../components/MyBookingCard.vue';



const toast = useToast();
const userStore = useUserStore()


const bookings = ref([])



const getBookings = async () => {

  try {
    const response = await axios.get(`/bookings/${parseInt(userStore.user.id)}`)
    bookings.value = response.data


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


onMounted(
  getBookings
)








</script>

<template>
  <div class="container ">
    <h1 class="text-center mt-4 mb-5">My Bookings</h1>
    <MyBookingCard v-for="b in bookings" :data="b" />
  </div>
</template>

<style scoped>
.container {
  padding-bottom: 50px;
}
</style>