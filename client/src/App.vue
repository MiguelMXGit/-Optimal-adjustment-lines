<template>
  <div id="app">
    <app-header />
    <router-view />
  </div>
</template>

<script>
import Header from '@/components/header/Header.vue';
export default {
  created() {
    this.$store.dispatch('auth/autoLogin');
  },
  components: {
    AppHeader: Header,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
