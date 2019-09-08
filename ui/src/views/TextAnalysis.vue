<template>
  <v-container
    fill-height
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col cols="12">
        <material-card
          color="green"
          title="Text analysis"
          text="Visualization fundamental text analysis"
        >
          <v-textarea
          outlined
          name="input-7-4"
          label="Text to be analyzed"
          value="Input here"
          v-model="inputText"
          ></v-textarea>
          <v-btn color="primary" v-on:click="analyze">Submit</v-btn>

          <div id="hierplane-container"></div>
        </material-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

  const axios = require('axios')
  // TODO: parameterize connection settings
  const host = process.env.VUE_APP_SERVER_HOST || 'http://localhost'
  const port = process.env.VUE_APP_SERVER_PORT || 5000
  const endpoint = host + ':' + port + '/text_analyze'

  export default {
    data: () => ({
      inputText: ''
    }),
    mounted () {
      // TODO: use static external js/css script
      let recaptchaScript = document.createElement('script')
      recaptchaScript.setAttribute('src', 'https://unpkg.com/hierplane/dist/static/hierplane.min.js')
      document.head.appendChild(recaptchaScript)

      let style = document.createElement('link')
      style.setAttribute('rel', 'stylesheet')
      style.setAttribute('type', 'text/css')
      style.setAttribute('href', 'https://unpkg.com/hierplane/dist/static/hierplane.min.css')
      document.head.appendChild(style)
    },
    methods: {
      renderTree (tree) {
        // FIXME
        hierplane.renderTree(tree, { target: '#hierplane-container', theme: 'light' })
      },

      analyze () {
        axios({
          method: 'post',
          url: endpoint,
          data: {
            input_text: this.inputText
          }
        }).then(res => {
          this.renderTree(res.data.tree)
        })
      }
    }
  }
</script>

<style lang="scss">
</style>
