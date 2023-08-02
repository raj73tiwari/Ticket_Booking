<script setup>

import { ref,defineProps } from 'vue';

const props = defineProps(['show'])
const show = {
  name: 'Music Festival',
  price: '$40',
  tickets: 100,
  rating: 4.8,
  tags: ['Music', 'Festival', 'Live'],
  time: '7:30 PM',
  image: '../assets/img/ppic.png',
  booked: false,
}
 
const booked=ref(false)
      
     
  


</script>


<template>
    <div class="show-card dark-theme">
        
      <div class="show-image">
        <img src='../assets/img/ppic.png' alt="Show Image" />
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
              {{ show.tickets }}
            </p>
            <p class="show-rating">
              <i class="bi bi-star icon " style="color: rgb(194, 194, 48);"></i>
              {{ show.rating }}
            </p>
          </div>
        </div>
        <div class="show-tags">
          <span v-for="(tag, index) in show.tags" :key="index" class="tag">{{ tag }}</span>
        </div>
      </div>
    </div>
    <div class="col-4">
      <div class="show-action">
       
          <button
            class="book-button"
            :class="{ 'booked-button': booked }"
            @click="booked=!booked"
          >
          <i v-if="booked" class="bi bi-bookmark-check me-1" style="color: #639138; font-size: 15px;"></i>
          <i v-else class="bi bi-bookmark me-1"></i>
            {{ booked ? 'Booked' : 'Book' }}
          </button>
          <p class="show-time">
            <i class="bi bi-clock icon" style="  color: #3a8fa7; font-size: 20px;"></i>
            {{ show.time }}
          </p>
        </div>
    </div>
</div>
    </div>
    </div>



   
  </template>
  
  <style >
.show-action{
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin-top: 35px;
}
  .conatin{
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
    height:180px ;
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
    color:bisque
   
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
  