
class Document {
  constructor (results) {
    this.results = results
    this.items = []
    this.lastParagraph = ''
  }
  process () {
    this.addItems()
    return this
  }
  addItem (item) {
    // show result item to user
    const sk = item.sk
    const pk = item.pk
    const data = item.data
    // const type = item.type
    const type = 'PARAGRAPH'
    // const description = this.highlight(item.data)
    // this.feedBack('hi' + JSON.stringify(item))
    // {sk: "s#00892#000951", pk: "d#002", data: "Page 20", type: "SENTENCE"}
    const parts = item.sk.split('#')
    if (parts[1] !== this.lastParagraph) {
      this.items.push({
        sk,
        pk,
        data,
        type
      })
    } else {
      this.items[this.items.length - 1].data += '. ' + item.data
    }
    this.lastParagraph = parts[1]
  }
  addItems () {
    // break down result into managable chunks
    // merge items in the same pargraph to one item
    let item = 0
    for (item in this.results) {
      if (this.results[item].type === 'SENTENCE') {
        this.addItem(this.results[item])
      }
    }
    /* eslint-disable no-console */
    console.log('addItems out')
    /* eslint-enable no-console */
    return this
  }
  getItems () {
    return this.items
  }
}
export { Document }
