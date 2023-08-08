<script setup>




const props = defineProps(['data'])



function getImageUrl(imageFilename) {
  return `http://localhost:5000/uploads/${imageFilename}`;
}






</script>


<template>
  <div class="show-car">

    <div class="show-image">
      <img :src="getImageUrl(data.show_image)" alt="Show Image" />
    </div>
    <div class="contain">
      <div class="row">
        <div class="col-8">
          <div class="show-details">
            <div class="show-header">
              <h1 class="show-name">{{ data.show_name }}</h1>
            </div>
            <div class="show-info">
              <div class="show-row">
                <p class="show-price">
                  <i class="bi bi-currency-dollar icon" style="color: rgb(144, 192, 72);"></i>
                  {{ data.show_price }}
                </p>
                <p class="show-rating">
                  <i class="bi bi-star icon " style="color: rgb(194, 194, 48);"></i>
                  {{ data.show_rating }}
                </p>
                <p class="show-time" style="font-size: 15px; ">
                  <i class="bi bi-clock icon" style="  color: #f08ace; font-size: 15px;"></i>
                  {{ data.show_time }}
                </p>
              </div>
            </div>
            <div class="show-tags">
              <span v-for="tag in data.show_tags.split(',')" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
        <div class="col-4">

          <div class="t_name">
            {{ data.theatre_name }}
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
  
<style >
.t_name {
  height: 20%;
  width: 100%;
  background-color: #4F5013;
  border-radius: .5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: bisque;
}

.col-4 {
  display: flex;
  align-items: center;
  justify-content: center;
}

.show-car {
  display: grid;
  grid-template-columns: 1fr 2fr;
  background-color: #0d1929;
  color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 16px;
  width: 100%;
  margin-bottom: 3%;
}
</style>
  