<template>
  <div class="ph-color-field">
    <div class="ph-header">
      <h4>
        {{ title }}
      </h4>
      <md-button class="md-icon-button" @click="reset">
        <md-icon>
          replay
        </md-icon>
      </md-button>
    </div>
    <color-picker :value="value || '#000'" @input="update"></color-picker>
  </div>
</template>

<script>
import ColorPicker from "vue-color/src/components/Chrome.vue";

export default {
  name: "ColorField",
  props: ["title", "id", "value", "default"],
  components: {
    ColorPicker,
  },
  data() {
    return {
      color: null,
      timer: null,
    };
  },
  methods: {
    reset() {
      this.$emit("reset", this.id);
    },
    update(color) {
      if (this.timer) {
        clearTimeout(this.timer);
      }

      this.$emit("color_changing");
      this.timer = setTimeout(
        () => this.$emit("color_changed", { id: this.id, hex: color.hex }),
        500
      );
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../../config/variables.scss";

.ph-color-field {
  flex: 0 50%;
  flex-direction: column;
  display: flex;
  align-items: center;

  background-color: var(--background-secondary-color);
  color: var(--foreground-primary-color);

  margin-bottom: 2em;
  padding-bottom: 1em;

  .ph-header {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
