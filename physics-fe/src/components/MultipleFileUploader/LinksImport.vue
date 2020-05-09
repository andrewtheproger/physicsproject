<template>
  <div class="mfu-links-import">
    <md-field>
      <label>...вставьте ссылку</label>
      <md-input
        @paste.prevent="onPaste"
        class="mfu-filelink-input"
        type="text"
      ></md-input>
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
          <img :src="link" alt="img" />
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
  props: ["links"],
  methods: {
    onPaste(e) {
      const value = e.clipboardData.getData("Text").trim();

      if (this.links.includes(value)) {
        return;
      }

      this.$emit("link_added", value);
    },
    removeLink(e) {
      const value = e.target.dataset.link;

      this.$emit("link_removed", value);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../config/variables.scss";

.mfu-links-import {
  display: flex;
  flex-direction: column;
  width: 50%;

  .mfu-previews span {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    .slide-fade-enter-active {
      transition: all 0.3s ease;
    }

    .slide-fade-leave-active {
      transition: all 0.3s ease;
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
      transition: all 0.2s ease-out;

      &:after {
        display: none;
        content: "X";
        font-size: 3em;
        color: var(--foreground-error-color);
        cursor: pointer;

        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;

        background-color: alpha(var(--background-primary-color), 0.3);
      }

      &:hover:after {
        display: flex;
        justify-content: center;
        align-items: center;
      }
    }
  }
}
</style>
