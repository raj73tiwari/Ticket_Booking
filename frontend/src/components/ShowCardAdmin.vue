<script setup>

import { ref } from 'vue';
import Alert from '../components/Alert.vue';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import ShowForm from './ShowForm.vue';

const toast = useToast();

const props = defineProps(['show'])
const emit = defineEmits(['changed'])

function getImageUrl(imageFilename) {
    return `http://localhost:5000/uploads/${imageFilename}`;
}

const isDelete = ref(false)
const isUpdate = ref(false)


const handleUpdate = async (val) => {
    isUpdate.value = !isUpdate.value
    if (val) {
        emit('changed')
    }

}

const handleDelete = async (val) => {
    isDelete.value = !isDelete.value
    if (val) {
        try {
            const response = await axios.post(`/deleteShow/${parseInt(props.show.id)}`)
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
}

</script>


<template>
    <div class="show-card dark-theme">
        <ShowForm v-if="isUpdate" :show="show" @closed="handleUpdate" />
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

                    <Alert v-if="isDelete" @closed="handleDelete" />
                    <button class="book-button" @click="isUpdate = !isUpdate">
                        <i class="bi bi-arrow-up-circle me-2"></i>
                        Update
                    </button>
                    <button class="book-button" style="background-color: rgb(196, 66, 66);" @click="isDelete = !isDelete">
                        <i class="bi bi-trash me-2"></i>
                        Delete
                    </button>


                </div>
            </div>
        </div>
    </div>
</template>
  
<style scoped>
.col-4 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 1.5rem;

}

.contai {
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: rgba(4, 0, 5, 0.95);
    z-index: 10;
    display: flex;

}
</style>
 
  