import { ref } from "vue";
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {

    const user = ref(null)

    function setUser(data) {
        user.value = data
    }
    function removeUser() {
        user.value = null
    }
    function isUser() {
        if (user.value == null) {
            return false
        }
        return true
    }
    function isAdmin() {
        if (user.value && user.value['is_admin']) {
            return true
        }
        return false
    }

    return {
        user,
        isUser,
        isAdmin,
        setUser,
        removeUser
    }


}, { persist: true })