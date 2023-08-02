<script setup>
import { ref } from 'vue';
import Im from '../assets/img/pholder.jpg'
import axios from 'axios';
import { useToast } from 'vue-toastification';
const toast = useToast();


const emit = defineEmits(['closed'])
const props = defineProps({
    show: {
        type: Object
    }
})
function getImageUrl(imageFilename) {
    return `http://localhost:5000/uploads/${imageFilename}`;
}


const name = ref('')
const tags = ref(null)
const rating = ref('')
const img = ref(Im)
const up_img = ref(null)
if (props.show) {
    name.value = props.show.name
    tags.value = props.show.tags
    rating.value = props.show.rating
    img.value = getImageUrl(props.show.image_name)
}


const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            if (props.show) {
                up_img.value = reader.result
            }
            img.value = reader.result;
        };
        reader.readAsDataURL(file);
    }

}

const handleSubmit = async () => {
    if (!props.show) {


        try {
            const response = await axios.post('createShow', {
                img: img.value,
                name: name.value,
                rating: rating.value,
                tags: tags.value
            });
            toast.success(response.data.message);
            emit('closed', true)

        }
        catch (error) {
            if (error.response && (error.response.status == 422 || error.response.status == 406)) {
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
    else {
        try {
            const response = await axios.post(`updateShow/${props.show.id}`, {
                img: up_img.value,
                name: name.value,
                rating: rating.value,
                tags: tags.value
            });
            toast.success(response.data.message);
            emit('closed', true)

        }
        catch (error) {
            if (error.response && (error.response.status == 422 || error.response.status == 406 || error.response.status == 404)) {
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
    <div class="cont">

        <h1 v-if="props.show" class="mb-4 mt-4">Update Show</h1>
        <h1 v-else class="mb-4 mt-4">Create Show</h1>

       


        <div class="show-card dark-theme">

            <div class="show-image">
                <img :src="img" alt="Show Image" />
                <label For="photo-upload" className="custom-file-upload "></label>
                <input type="file" accept=".jpeg,.jpg,.png" id="photo-upload" @change="handleUpload">
            </div>
            <div class="contain">
                
                        <div class="show-details">
                            <div class="show-header">
                                <input type="text" class="form-control mb-1 " id="inputName" v-model="name"
                    placeholder="Enter Show Name">
                            </div>
                            <div class="show-info">
                                <div class="show-row">
                                    
                                    
                                    <p class="show-rating">
                                        <i class="bi bi-star icon " style="color: rgb(194, 194, 48);"></i>
                                 
                                    </p>
                                    <input type="number"  class="form-control mb-1 mt-1" id="inputNumber" v-model="rating" placeholder="Enter Rating"
                        style="max-width: 30%;">
                                </div>
                            </div>
                            <div class="show-tags">
                                <span class="tag">tags :</span>
                                <input type="text"  class="form-control ms-4" id="inputTags" v-model="tags" placeholder="Enter Tags (CSV)"
                        style="max-width: 70%;">
                            </div>
                        </div>
                   
            </div>
        </div>












        <div class="buttons">
            <button type="button" class="submit me-5" @click="handleSubmit">&nbsp;{{ props.show ? 'Update' : 'Create'
            }}&nbsp;</button>
            <button type="button" class="submitt" @click="emit('closed', false)">&nbsp;Close&nbsp;</button>
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
    height: 100%;
    background-color: rgba(4, 0, 5, 0.95);
    z-index: 10;
    display: flex;

}

input[type="file"] {
    display: none;
}



.show-image {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.custom-file-upload {
    cursor: pointer;
    position: absolute;
    width: 100%;
    height: 100%;
}




::placeholder {
    color: antiquewhite;
    opacity: 0.5;
}

input {
    background-color: #202124;
    border-color: transparent;
    color: aliceblue;
}

input:focus {
    background-color: #202124;
    border-color: #021729;
    box-shadow: 0px 0px 8px 3px rgba(19, 9, 73, 0.3);
    color: aliceblue;
}

.submit {
    border-radius: 2rem;
    /* ....background: linear-gradient(to left, #03B3E3 0%, #0E9B71 100%); */

    background: linear-gradient(90deg, #0E9B71, transparent) #2196f3;
    color: #fff;
    text-decoration: none;
    transition: background-color 1s;
    border: none;
    padding: 8px;
    min-width: 7rem;
    margin-top: 10px;

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

.submit:hover {
    background-color: #3f51b5;
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





img {
    max-width: 100%;
    height: 225px;
    position: relative;

}
</style>