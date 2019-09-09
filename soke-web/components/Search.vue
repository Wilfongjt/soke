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
        <span>
          <button :disabled="form.submitStatus === 'PENDING'" class="button" type="submit">
            Submit!
          </button>
        </span>
      </p>
    </form>
    <!-- Search Result -->
    <div v-for="item in page.items" :key="item.id">
      <span>&nbsp;</span>
      <p class="subtitle">
        <!-- nuxt-link to="/about">{{ item.title }}</nuxt-link -->
        <a href="#" @click="onClick(item)">{{ item.title }}</a>
      </p>
      <p>
        <span v-html="item.description" />
      </p>
    </div>
  </div>
</template>

<script>
import { AWSHandlers } from './mixins/AWSHandlers.js'

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
      },
      session: {
        authorizationToken: 'Authorization'
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
    awsGuestHeader () {
      return {
        'Content-Type': 'application/json'
      }
    },
    awsGuestBody () {
      return process.env.GUEST
    },
    awsGatewayHeader () {
      return {
        'Content-Type': 'application/json',
        'Authorization': this.session.authorizationToken
      }
    },
    awsGatewayBodyDocument () {

    },
    awsGatewayBody () {
      return this.form
    },
    awsGatewayURL () {
      // no keywords
      return process.env.INDEX
    }
  },
  mounted () {
    // at this point we want to make a guest connection to our services
    this.awsHandlers.awsSignIn(process.env.SIGNIN, this.awsGuestHeader, this.awsGuestBody)
      .then((response) => {
        if (response.status === 200) {
          this.session.authorizationToken = response.data.token
          // check for results field
          this.feedBack('Type another!')
          this.addItem({
            title: 'Ready',
            data: this.session.authorizationToken ? 'Go' : 'Unauthorized'
          })
        } else {
          this.feedBack('Something unexpected happened!')
          this.log('Something unexpected happened!')
          this.session.authorizationToken = 'Authorization'
        }
      })
      .catch((err) => {
        this.feedBack('Guest Sign In is disturbingly incorrect (%s)'.replace('%s', err))
        this.log('Guest Sign In is disturbingly incorrect (%s)'.replace('%s', err))
        this.session.authorizationToken = 'Authorization'
      })
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
    onClick (item) {
      this.feedBack(item.pk)
      this.awsHandlers.awsDocument(process.env.DOCUMENT, this.awsGatewayHeader, this.awsGatewayBodyDocument)
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
            this.feedBack('Whoa, I did not set this comming (%s)!'.replace('%s', response.status))
            this.log('Whoa, I did not see this comming (%s)!'.replace('%s', response.status))
          }
        })
        .catch((err) => {
          this.feedBack('Something unexpected happened (%s)!'.replace('%s', err))
          this.log('Something unexpected happened (%s)!'.replace('%s', err))
        })
    },
    onSubmit () { // submit button
      // no words then no searches
      if (this.form.words === null || this.form.words === undefined || this.form.words.length === 0) {
        this.feedBack('Type one or more words!')
        return
      }
      // clear the list
      // this.page.items = []
      this.page.items.length = 0
      // make the call
      this.awsHandlers.awsIndex(this.awsGatewayURL, this.awsGatewayHeader, this.awsGatewayBody)
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
            this.feedBack('Whoa, I did not set this comming (%s)!'.replace('%s', response.status))
            this.log('Whoa, I did not see this comming (%s)!'.replace('%s', response.status))
          }
        })
        .catch((err) => {
          this.feedBack('Something unexpected happened (%s)!'.replace('%s', err))
          this.log('Something unexpected happened (%s)!'.replace('%s', err))
        })
    },
    addItem (item) {
      // show result item to user
      const id = this.page.items.length + 1
      const pk = item.pk
      const title = item.title
      const description = this.highlight(item.data)
      // this.feedBack('hi' + JSON.stringify(item))
      this.page.items.push({
        id,
        pk,
        title,
        description
      })
    },
    addItems (itemArray) {
      // break down result into managable chunks
      let i = 0
      for (i = 0; i < itemArray.length; i++) {
        this.feedBack('hi' + JSON.stringify(itemArray[i]))
        this.addItem(itemArray[i])
      }
    }
  } // methods
}
</script>

<style scoped>
.band {
  width: 100%;
}

</style>
