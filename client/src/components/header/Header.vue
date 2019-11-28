<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Líneas de ajuste óptimo</a>
    <button class="btn btn-outline-success my-2 my-sm-0" v-if="isAuth" v-on:click="onLogout">
      Log Out
    </button>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Header',
  computed: {
    ...mapGetters('auth', {
      isAuth: 'isAuthenticated',
    }),
  },
  methods: {
    onLogout() {
      this.$store.dispatch('auth/logout');
    },
  },
};
</script>
