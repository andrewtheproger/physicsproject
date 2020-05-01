<template>
    <div class="ph-userpage">
        <Logout></Logout>
    </div>
</template>

<script>
import config from "../config/api.js";
import Logout from "./Logout";
export default {
    name: "Userpage",
    components: {
        Logout
    },
    computed: {
        logout () {
            return config.apiPrefix + "/users/logout";
        }
    },
    data() {
        return {

        }
    },
    methods: {
    }
};
</script>

<style lang="scss" scoped>
    @import "../config/variables.scss";

</style>
