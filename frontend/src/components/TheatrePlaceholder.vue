<script setup>


</script>

<template>
  <div class="card" style="width: 18rem;">
    <img src="../assets/img/placeholder.png" class="card-img-top" alt="...">
    <div class="card-body">
      <h5 class="card-title placeholder-glow">
        <span class="placeholder col-7"></span>
      </h5>
      <p class="card-text placeholder-glow">
        <span class="placeholder col-6"></span>
      </p>
      <p class="card-text placeholder-glow">
        <span class="placeholder col-8"></span>
      </p>
    </div>
  </div>
</template>

<style scoped>
.card {
  background-color: #021729;
  cursor: pointer;
  margin: 0 3.5% 4% 3.5%;
  transition: all .3s ease-in-out;


}

.card:hover {
  transform: translate3d(0px, -2px, 0px);
}

h3,
h5 {
  color: white;
}

p {
  color: #9B9C9E;
  margin-bottom: 2px;
}

.card-body {
  padding: 8px;

}

img {
  padding: 1%;
  max-width: 100%;
  height: 150px;

}</style>