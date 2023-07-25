<script setup>
import {useRouter} from "vue-router"
const router=useRouter()
const toTheatre=()=>{
    router.push(`/theatre/${props.id}`)
}
function getImageUrl(imageFilename) {
  return `http://localhost:5000/uploads/${imageFilename}`;
}

const props = defineProps({
    id:{
        type:Number
    },
    name: {
        type: String,
    },
    img: {
        type: String
    },
    seat: {
        type: Number
    },
    address:{
      type:String
    }
})

</script>

<template>
<div class="card" style="width: 18rem;" @click="toTheatre" >
  <img :src="getImageUrl(props.img)"  class="card-img-top" alt="...">
  <div class="card-body">
    <h3 class="card-title mb-2">{{ props.name }}</h3>
    <p class="card-text"><i class="bi bi-shop-window me-2 ms-1"></i>Tickets Available: {{ props.seat }}</p>
    <p class="card-text"><i class="bi bi-geo-alt me-2 ms-1"></i>{{ props.address }}</p>
  </div>
</div>
</template>

<style scoped>
.card{
    background-color:  #021729;
    cursor: pointer;
    margin: 0 3.5% 4% 3.5%;
    transition: all .3s ease-in-out;
    
    
}
.card:hover {
  transform: translate3d(0px, -2px, 0px);
}
h3{
    color: white;
}
p{
    color: #9B9C9E;
    margin-bottom: 2px;
}

.card-body{
    padding: 8px;
    
}
img{
    padding: 1%;
    max-width: 100%;
    height: 150px ;

}

</style>