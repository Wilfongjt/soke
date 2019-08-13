<template>
  <div id="search" class="band">
    <h1 class="title">
      {{ page.title }}
    </h1>

    <form id="search" @submit.prevent="onSubmit">
      <p>
        <label for="form.words" class="subtitle">{{ page.subtitle }}</label>
      </p>
      <p>
        <input id="words" v-model="form.words" placeholder="words">
      </p>
      <p>
        <!-- span>
          <button class="button" type="button" @click="wordMe();">
            Word Me
          </button>
        </span -->
        <span>
          <button :disabled="form.submitStatus === 'PENDING'" class="button" type="submit">
            Submit!
          </button>
        </span>
      </p>
    </form>
    <!--ul id="search-results"-->
    <div v-for="item in page.items" :key="item.id">
      <span>&nbsp;</span>
      <p class="subtitle">
        {{ item.title }}
      </p>
      <p>
        <span v-html="item.description" />
      </p>
    </div>
    <!--/ul-->
  </div>
</template>

<script>
import { AWSHandlers } from './mixins/AWSHandlers.js'
// if (process.env.NODE_ENV !== 'production') require('dotenv').config()

export default {

  data () {
    return {
      form: {
        words: ''
      },
      submitStatus: 'PENDING',
      page: {
        title: 'Soke',
        subtitle: 'Type a word!',
        items: []
      }
    }
  },
  computed: {
    wordList () {
      return this.form.words.split(' ')
    },
    awsHandlers () {
      return new AWSHandlers(this)
    },
    awsHeader () {
      return {
        'x-api-key': process.env.APIKEY
      }
    },
    awsGatewayParameters () {
      return 'keywords=%s'.replace('%s', this.form.words)
    },
    awsSearchURL () {
      // no keywords
      if (this.form.words === null || this.form.words === undefined || this.form.words.length === 0) {
        return process.env.INDEX
      }
      return '%s?%p'
        .replace('%s', process.env.INDEX)
        .replace('%p', this.awsGatewayParameters)
    }
  },
  methods: {
    log (msg) {
      /* eslint-disable no-console */
      console.log(msg)
      /* eslint-enable no-console */
    },
    feedBack (msg) {
      this.page.subtitle = msg
    },
    wordMe () {
      this.form.words = 'dog '
    },
    highlight (description) {
      let desc = description
      let i = 0
      for (i in this.wordList) {
        desc = desc.replace(
          this.wordList[i] + ' ',
          '<strong>%s</strong>'.replace('%s', this.wordList[i] + ' ')
        )
      }
      return desc
    },
    onSubmit () { // submit button
      // clear the list
      this.page.items = []
      // make the call
      this.awsHandlers.awsGET(this.awsSearchURL, this.awsHeader)
        .then((response) => {
          if (response.status === 200) {
            let i = 0
            // check for results field
            if (response.data.hasOwnProperty('results')) {
              for (i = 0; i < response.data.results.length; i++) {
                this.addItems(response.data.results[i].Items)
              }
            } else {
              this.log('no results for (%s)'.replace('%s', this.form.words))
            }
            this.feedBack('Type another!')
          } else {
            this.feedBack('Something unexpected happened!')
          }
        })
        .catch((err) => {
          this.log('submit error: ' + err)
        })
    },
    addItem (item) {
      // show result item to user
      const id = this.page.items.length + 1
      const title = item.title
      const description = this.highlight(item.data)
      this.page.items.push({
        id,
        title,
        description
      })
    },
    addItems (itemArray) {
      // break down result into managable chunks
      let i = 0
      for (i = 0; i < itemArray.length; i++) {
        this.addItem(itemArray[i])
      }
    }
  }
}
</script>

<style scoped>
.band {
  width: 100%;
}

</style>
