<template>
  <div class="mfu-links-import">
    <md-field>
      <label>...вставьте ссылку</label>
      <md-input @paste.prevent="onPaste" class="mfu-filelink-input" type="text"></md-input>
    </md-field>

    <ul class="mfu-previews">
      <transition-group name="slide-fade" mode="out-in">
        <li 
          class="mfu-preview"
          v-for="(link, i) in links" 
          :key="`link-${i}`"
          :data-link="link"
          @click="removeLink"
          >
            <img :src="link" alt="img"  />
        </li>
      </transition-group>
    </ul>
  </div>
</template>


<script>
require("es6-promise").polyfill();
import axios from "axios";
{
  axios;
}
export default {
  data() {
    return {
      links: []
    };
  },
  methods: {
    onPaste(e) {
      const value = e.clipboardData.getData('Text').trim()

      if (this.links.includes(value)) {
        return;
      }

      this.links = [...this.links, value]
    },
    removeLink(e) {
      const value = e.target.dataset.link;

      this.links = this.links.filter(x => x !== value)
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../config/variables.scss";

.mfu-links-import {
  display: flex;
  flex-direction: column;
  width: 50%;

  .mfu-previews span{
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    .slide-fade-enter-active {
      transition: all .3s ease;
    }

    .slide-fade-leave-active {
      transition: all .3s ease;
    }

    .slide-fade-enter {
      transform: translateY(-100px);
      opacity: 0;
    }

    .slide-fade-leave-to {
      transform: translateY(100px);
      opacity: 0; 
    }

    .mfu-preview {
      margin: 3px;
      width: 30%;
      position: relative;
      transition: all 1 easy;

      &:after {
        display: none;
        content: 'X';
        font-size: 3em;
        color: #d00;
        cursor: pointer;

        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        
        background-color: rgba(0,0,0,0.2);
      }

      &:hover {
        &:after {
          display: flex;
          justify-content: center;
          align-items: center;
        }
      }
    }
  }
}

.md-field,
.md-field.md-theme-default.md-focused,
.md-field.md-theme-default.md-has-value {
  .md-input,
  label {
    color: inherit;
    -webkit-text-fill-color: inherit;
  }


  &:hover:after {
    background-color: $secondary-fg-color;
    transition: all .3s;
  }

  max-height: 3em;
}

.md-field.md-theme-default label,
.md-icon.md-theme-default.md-icon-font {
  color: inherit;
}

.md-field.md-theme-default label {
  padding-left: 1em;
}
</style>
