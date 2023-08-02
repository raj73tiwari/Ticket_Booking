<script setup>

const props=defineProps({
  theatres:{
    default:null
  },
  users:{
    default:null
  },
  shows:{
    default:null
  },
})


</script>


<template>

<table class="table table-success table-striped">
    <thead>
    <tr v-if="props.theatres" >
      <th scope="col">ID</th>
      <th scope="col">Name</th>
      <th scope="col">Capacity</th>
      <th scope="col">Address</th>
    </tr>
    <tr v-if="props.users">
      <th scope="col">ID</th>
      <th scope="col">User Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    <tr v-if="props.theatres"  v-for="t in theatres">
      <td >{{ t.id }}</td>
      <td>{{ t.name }}</td>
      <td>{{ t.capacity }}</td>
      <td>{{ t.address }}</td>
    </tr>
  </tbody>
</table>

</template>

<style scoped>


</style>