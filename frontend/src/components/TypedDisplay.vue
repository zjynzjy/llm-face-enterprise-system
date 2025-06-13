<template>
  <div v-if="html" v-html="displayedHtml"></div>
  <div v-else>{{ displayedText }}</div>
</template>

<script>
import MarkdownIt from 'markdown-it'

export default {
  props: {
    text: {
      type: String,
      required: true
    },
    speed: {
      type: Number,
      default: 30
    },
    html: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      displayedText: '',
      displayedHtml: '',
      fullText: '',
      currentIndex: 0,
      timer: null,
      md: new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true
      })
    }
  },
  watch: {
    text: {
      immediate: true,
      handler(newText) {
        this.reset()
        this.fullText = newText
        this.startTyping()
      }
    }
  },
  methods: {
    reset() {
      clearInterval(this.timer)
      this.displayedText = ''
      this.displayedHtml = ''
      this.currentIndex = 0
    },
    startTyping() {
      this.timer = setInterval(() => {
        if (this.currentIndex < this.fullText.length) {
          this.currentIndex++
          this.displayedText = this.fullText.substring(0, this.currentIndex)
          
          // 如果需要渲染HTML，则将当前文本转换为Markdown HTML
          if (this.html) {
            this.displayedHtml = this.md.render(this.displayedText)
          }
        } else {
          clearInterval(this.timer)
        }
      }, this.speed)
    }
  },
  beforeUnmount() {
    clearInterval(this.timer)
  }
}
</script>