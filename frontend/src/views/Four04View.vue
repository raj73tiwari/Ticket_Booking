<template>
  <div class="container">
    <h1>404</h1>
<h3>The page you are looking for cannot be found</h3>
</div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css?family=Alfa+Slab+One|Josefin+Slab');


@keyframes darken {
  0%{ font-size: 100px;  color:#566573;}
  50%{font-size: 200px; color:#273746}
  100% {font-size: 250px; color:#17202a}
}
  
.container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 85vh;
}
h1 {
  font-family: 'Alfa Slab One', cursive;
  margin: 0 auto;
  display:block;
  text-align: center;
  animation-name: darken;
  animation-duration: 5s;
  animation-iteration-count: infinite;
}

h3 {
  font-family: 'Josefin Slab', serif;
  margin: 0 auto;
  display:block;
  text-align: center;
  font-size: 30px;
}
</style>