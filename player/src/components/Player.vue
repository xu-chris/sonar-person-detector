<template>
  <Media
    :kind="'video'"
    :controls="false"
    :src="source"
    :autoplay="true"
    :style="{width: '100%'}"
    @canplay="onCanPlayThrough($event)"
  />
  <!-- <video
    id="player"
    autoplay="autoplay"
    muted="muted"
    loop="loop"
    playsinline="playsinline"
    preload="metadata"
    data-aos="fade-up"
    v-on:canplay="onCanPlayThrough"
  >
    <source :src="source"
            :type="type">
      Your browser does not support MP4 Format videos or HTML5 Video.
  </video> -->
</template>

<style scoped>
#player {
  width: 100%;
  height: 100%
}
</style>

<script>
import axios from 'axios'
import Media from '@dongido/vue-viaudio'
import { setTimeout } from 'timers'

export default {
  name: 'Player',
  components: {
    Media
  },
  beforeMount () {
    this.getState()
    this.reload()
  },
  data () {
    return {
      source: '',
      type: 'video/mp4',
      state: 'stop'
    }
  },
  methods: {
    onCanPlayThrough (event) {
      event.target.muted = true
      event.target.play()
      event.target.pause()
      event.target.play()
    },

    actByState (state) {
      if (state !== 'stop') {
        this.source = state + '.mp4'
      } else {
        this.source = ''
      }
    },

    getState () {
      axios.get('/current/')
        .then(response => {
          let state = response.data['state']

          if (state !== this.state) {
            this.actByState(state)
            this.state = state
            console.log('New state: ' + state)
          }
        })
        .catch(e => {
          console.log(e)
        })
    },

    reload () {
      setTimeout(function () {
        this.getState()
        this.reload()
      }.bind(this), 1000)
    }
  }
}
</script>
