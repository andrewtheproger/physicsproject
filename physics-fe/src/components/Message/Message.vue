<template>
  <div :class="this.getClass()">
    <div class="ph-message-icons">
      <md-icon v-if="this.severity === 'success'">done</md-icon>
      <md-icon v-if="this.severity === 'warning'">report_problem</md-icon>
      <md-icon v-if="this.severity === 'error'">clear</md-icon>
    </div>
    <md-divider class="md-inset"></md-divider>
    <span class="ph-message-content">{{text}}</span>
  </div>
</template>

<script>
  export default {
    name: "Message",
    props: ["text", "severity"],
    methods: {
      getClass: function () {
        const defaultClass = "ph-message";
        switch (this.severity) {
          case "success":
            return `${defaultClass} ph-success-message`;
          case "warning":
            return `${defaultClass} ph-warning-message`;
          case "error":
            return `${defaultClass} ph-error-message`;
          default:
            return defaultClass;
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
.ph-message {
  border-radius: 5px;
  padding: 0.2em 0.5em;

  overflow: hidden;
  word-wrap: break-word;

  .md-icon {
    margin-right: 1em;
  }
}

.ph-success-message {
  background-color: var(--background-success-color);
  color: var(--foreground-success-color);

  i.md-icon.md-theme-default.md-icon-font {
    color: var(--foreground-success-color);
  }

  .ph-message-icons {
    border-bottom: 1px solid var(--foreground-success-color);
    padding-bottom: 0.5em;
  }
}

.ph-warning-message {
  background-color: var(--background-warning-color);
  color: var(--foreground-warning-color);

  i.md-icon.md-theme-default.md-icon-font {
    color: var(--foreground-warning-color);
  }

  .ph-message-icons {
    border-bottom: 1px solid var(--foreground-warning-color);
    padding-bottom: 0.5em;
  }
}

.ph-error-message {
  background-color: var(--background-error-color);
  color: var(--foreground-error-color);

  i.md-icon.md-theme-default.md-icon-font {
    color: var(--foreground-error-color);
  }

  .ph-message-icons {
    border-bottom: 1px solid var(--foreground-error-color);
    padding-bottom: 0.5em;
  }
}
</style>
