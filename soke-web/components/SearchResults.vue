<template>
  <h1>RESULTS</h1>

  </nav-->
</template>
<script>

export default {
  data () {
    return {
    page: {
      title: 'Search Results',
      subtitle: 'Type a word!',
      items: []
    },
      /* footer: {
        list: [
          {title: 'Github', href: 'https://github.com/citizenlabsgr'},
          {title: 'Slack', href: 'https://slack.com'}
        ]
      }
      */
    }
  }
}
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-flow:row wrap;
  justify-content: center;
  align-items: center;
}

li {
  margin: 20px 10px 0px 20px;
}

img {
  height: 50px
}
</style>
