<template>
  <video
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
  </video>
</template>

<style scoped>
#player {
  width: 100%;
  height: 100%
}
</style>

<script>
import { axios } from 'axios'
import { setTimeout } from 'timers'

export default {
  name: 'Player',
  beforeMount () {
    this.reload()
  },
  data () {
    return {
      source: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4',
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
      axios
        .get('/current/')
        .then(response => {
          let state = response.data['state']

          if (state !== this.state) {
            this.actByState(state)
            this.state = state
          }
        })
    },

    reload () {
      setTimeout(function () {
        this.getState()
      }.bind(this), 1000)
    }
  }
}
</script>
