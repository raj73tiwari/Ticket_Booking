<script setup>

const emit = defineEmits(['closed'])

</script>


<template>
    <div class="contai">
        <div class="myalert ">
            <h1 class="text-center mb-3 mt-2" style="font-weight: 900;">Confirm !</h1>

            <h4 class="text-center">are you sure ?</h4>
            <div class="buttons mt-5">
                <button class="close" @click="emit('closed',false)"><i class="bi bi-x-circle me-1"></i> Close</button>
                <button class="confirm"  @click="emit('closed',true)"   ><i class="bi bi-check-circle" ></i> Confirm</button>
            </div>
        </div>

    </div>
</template>


<style scoped>
.contai {
    display: flex;
    align-items: center;
    flex-direction: column;
    position: absolute; 
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(4, 0, 5, 0.95);
    z-index: 10;
    display: flex;

}

.close:hover {
    background: rgb(150, 78, 78);
}

.confirm{
    background-color: #28A745; 
    width: 30%;
    padding: 0%;
    margin-left: auto;
    margin-right: auto;
    
}
.confirm:hover {
    background: #0b6821;
}

button {
    width: 60%;
    height: 40px;
    margin: 10px auto;
    justify-content: center;
    display: block;
    color: #fff;
    background-color: #077;
    font-size: 1em;
    font-weight: bold;
    margin-top: 10px;
    outline: none;
    border: none;
    border-radius: 5px;
    transition: .2s ease-in;
    cursor: pointer;
}

.close {
    background-color: rgb(192, 113, 113);
    width: 30%;
    padding: 0%;
    margin-left: auto;
    margin-right: auto;
    



}

.myalert {
    height: 17rem;
    width: 27rem;
    padding-top: 1rem;
    padding-left: 3rem;
    padding-right: 3rem;
    border-radius: 0.5rem;
    background-color: #EEEEEE;
    color: rgb(150, 78, 78);
    position: relative;
    border: 1px solid;
    border-color: rgb(150, 78, 78);
    margin-top: 15%;


}

.buttons {
    display: flex;
    justify-content: center;
    align-items: center;

}
</style>