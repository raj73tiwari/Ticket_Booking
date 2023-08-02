<script setup>
import { ref,onMounted } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ShowListCard from './ShowListCard.vue';

const toast = useToast();

const props=defineProps(['t_id'])

const emit = defineEmits(['closed'])
const shows=ref(null)

const getShow = async () => {
  try {
    const response = await axios.get('/show')
    shows.value = response.data
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
    getShow
)


</script>

<template>
    <div class="cont">
        <div class="scrl">

        <h1  class="mb-4 mt-4">Add Shows</h1>
        
        <ShowListCard v-for="s in shows" :show="s" :t_id="t_id" @closed="emit('closed',true)"/>
        
        <div class="buttons mt-4 mb-4">
            <button type="button" class="submitt" @click="emit('closed', false)">&nbsp;Close&nbsp;</button>
        </div>
    </div>
    </div>
</template>
    

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Belanosima|Patua+One|Pacifico');


input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.cont {
    display: flex;
    align-items: center;
    flex-direction: column;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(4, 0, 5, 0.95);
    z-index: 10;
    display: flex;

}

.submitt {
    border-radius: 2rem;
    /* ....background: linear-gradient(to left, #03B3E3 0%, #0E9B71 100%); */

    background: linear-gradient(90deg, #9b0e1a, transparent) #d3313f;
    color: #fff;
    text-decoration: none;
    transition: background-color 1s;
    border: none;
    padding: 8px;
    min-width: 7rem;
    margin-top: 10px;

}

.scrl{
    display: flex;
    align-items: center;
    flex-direction: column;
    height: 90%;
    width: 90%;
    margin-top: 2%;
    border: 1px solid bisque;
    border-radius: 0.5rem;
    overflow-y: scroll;
}

.submitt:hover {
    background-color: #5e0a26;
}

h1 {
    font-family: 'Belanosima';
}

h4 {
    color: white;
}

p {
    color: #9B9C9E;
    margin-bottom: 2px;
}

::-webkit-scrollbar {
  width: 10px;
  
}

/* Track */
::-webkit-scrollbar-track {
  background:  #14021a;
  border-radius: 1rem; 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 1rem;

}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}



</style>