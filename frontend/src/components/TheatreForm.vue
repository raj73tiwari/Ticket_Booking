<script setup>
import { ref } from 'vue';
import Im from '../assets/img/pholder.jpg'
import axios from 'axios';
import { useToast } from 'vue-toastification';
const toast = useToast();


const emit = defineEmits(['closed'])
const props = defineProps({
    theatre: {
        type: Object
    }
})
function getImageUrl(imageFilename) {
    return `http://localhost:5000/uploads/${imageFilename}`;
}


const name = ref('')
const seat = ref(null)
const address = ref('')
const img = ref(Im)
const up_img = ref(null)
if (props.theatre) {
    name.value = props.theatre.name
    seat.value = props.theatre.capacity
    address.value = props.theatre.address
    img.value = getImageUrl(props.theatre.image_name)
}


const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            if (props.theatre) {
                up_img.value = reader.result
            }
            img.value = reader.result;
        };
        reader.readAsDataURL(file);
    }

}

const handleSubmit = async () => {
    if (!props.theatre) {


        try {
            const response = await axios.post('createTheatre', {
                img: img.value,
                name: name.value,
                address: address.value,
                seat: seat.value
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
            const response = await axios.post(`updateTheatre/${props.theatre.id}`, {
                img: up_img.value,
                name: name.value,
                address: address.value,
                seat: seat.value
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

        <h1 v-if="props.theatre" class="mb-4 mt-4">Update Theatre</h1>
        <h1 v-else class="mb-4 mt-4">Create Theatre</h1>

        <div class="card" style="width: 27rem;">

            <div class="bg">
                <img :src="img" class="card-img-top" alt="...">
                <label For="photo-upload" className="custom-file-upload "></label>
                <input type="file" accept=".jpeg,.jpg,.png" id="photo-upload" @change="handleUpload">
            </div>

            <div class="card-body">
                <input type="text" class="form-control mb-1 " id="inputName" v-model="name"
                    placeholder="Enter Theatre Name">
                <div class="addr">
                    <p class="card-text"><i class="bi bi-shop-window me-2 ms-1"></i>Seating Capacity :</p>
                    <input type="number" class="form-control mb-1 mt-1" id="inputNumber" v-model="seat" placeholder="Enter"
                        style="max-width: 40%; margin-left: 5%;">
                </div>

                <div class="addr">
                    <i class="bi bi-geo-alt me-2 ms-1"></i>
                    <input type="text" class="form-control mb-1 mt-1" id="inputAddress" v-model="address"
                        placeholder="Enter Theatre Address">
                </div>
            </div>
        </div>
        <div class="buttons">
            <button type="button" class="submit me-5" @click="handleSubmit">&nbsp;{{ props.theatre ? 'Update' : 'Create'
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



.bg {
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

.card {
    background-color: #010911;
    margin: 0 3.5% 2% 3.5%;
    transition: all .3s ease-in-out;
    position: relative;


}

.addr {
    display: flex;
    align-items: center;
    color: #9B9C9E
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

.card-body {
    padding: 8px;

}

.card-img-top {
    position: relative;
}

img {
    padding: 1%;
    max-width: 100%;
    height: 225px;
    position: relative;

}
</style>