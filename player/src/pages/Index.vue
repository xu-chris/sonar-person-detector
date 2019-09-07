<template>
  <div>
    <Player class="fixed-center" />
  </div>
</template>

<style>
body {
  background-color: black;
}
</style>

<script>
import Player from '../components/Player'

export default {
  name: 'PageIndex',
  components: {
    Player
  },
  data () {
    return {}
  }
}
</script>
