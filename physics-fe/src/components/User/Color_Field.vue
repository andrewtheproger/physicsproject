<template>
  <div class="ph-color-field">
    <h4>{{title}}</h4>
    <color-picker :value="value || '#000'" @input="update"></color-picker>
  </div>
</template>

<script>
    import ColorPicker from 'vue-color/src/components/Chrome.vue';

    export default {
        name: "ColorField",
        props: ['title', 'id', 'value'],
        components: {
            ColorPicker,
        },
        data() {
            return {
                color: null,
                timer: null
            };
        },
        methods: {
            update(color) {
                if (this.timer) {
                    clearTimeout(this.timer);
                }

                this.$emit('color_changing');
                this.timer = setTimeout(() => this.$emit('color_changed', {id: this.id, hex: color.hex}), 500)
            }
        }
    };
</script>
<style lang="scss" scoped>
  @import "../../config/variables.scss";

.ph-color-field {
  flex: 0 50%;
  flex-direction: column;
  display: flex;
  align-items: center;

  margin-bottom: 2em;
}
</style>
