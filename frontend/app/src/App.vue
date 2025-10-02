<template>
  <div class="app min-h-screen bg-gray-50">
    <generate-message></generate-message>
  </div>
</template>

<script>
import GenerateMessage from './components/GenerateMessage.vue'

export default {
  name: 'App',
  components: {
    GenerateMessage
  }
}
</script>
