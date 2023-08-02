<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';

const toast = useToast();
const props = defineProps(['show', 't_id'])
const emit = defineEmits(['closed'])

const time = ref(null)
const price = ref(null)

const isForm = ref(false)

const handleAdd = async() => {
    try {
        console.log(9878743897734)
        const response = await axios.post(`/addShow/${parseInt(props.t_id)}`, {
            show_id: props.show.id,
            price: price.value,
            time: time.value,

        });
        toast.success(response.data.message);
        emit('closed')

    }
    catch (error) {
        if (error.response && (error.response.status == 404 || error.response.status == 406)) {
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

</script>



<template>
    <div class="show-list">
        <div class="view1" v-if="!isForm">
            <div class="con1">
                <h1>{{ show.name }}</h1>
                <div class="show-tags">
                    <span v-for="tag in show.tags.split(',')" class="tag" style="background-color: rgb(87, 53, 119);">{{ tag
                    }}</span>

                </div>
            </div>
            <div class="con2">
                <div class="show-row">

                    <p class="show-rating">
                        <i class="bi bi-star icon " style="color: rgb(194, 194, 48);"></i>
                        {{ show.rating }}
                    </p>
                </div>
            </div>
            <div class="con3">
                <button class="book-button" style="background-color: rgb(79, 80, 19);" @click="isForm = !isForm">

                    Add
                    <i class="bi bi-caret-right-fill"></i>
                </button>
            </div>
        </div>
        <div class="view2" v-if="isForm">


            <p class="show-price" style="margin-right: 0%;">
                <i class="bi bi-currency-dollar icon" style="color: rgb(144, 192, 72);"></i>
                {{ show.price }}
            </p>
            <input type="number" class="form-control " id="inputName" v-model="price" placeholder="Ticket Price">

            <p class="show-tickets ms-3">
                <i class="bi bi-clock icon" style="color: rgb(228, 167, 88);"></i>
                {{ show.tickets }}
            </p>
            <input type="datetime-local" class="form-control mb-1 " id="inputName" v-model="time" placeholder="Show Time">

            <button class="book-button" style="background-color: rgb(41, 80, 19);" @click="handleAdd">
                <i class="bi bi-plus-circle me-2"></i>
                Add

            </button>

        </div>
    </div>
</template>


<style scoped>
.show-list {
    display: flex;
    height: 150px;
    width: 90%;
    border-radius: 0.5rem;
    background-color: #0f2d31;
    padding: 3%;
    margin: 1%;

}

input {
    width: 20%;
}

.view1,
.view2 {
    display: flex;
    justify-content: space-between;
    width: 100%;

}

.view2 {
    align-items: center;
}

p {
    font-size: 40px;
    margin: 0%;
}

h1 {
    color: bisque;
}

button {
    margin: 0%;
}

.con2,
.con3 {
    display: flex;
    align-items: center;
}

.con1 {
    display: flex;
    flex-direction: column;
    justify-content: center;
}</style>