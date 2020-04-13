<template>
  <div id="app">
    <header>
      <div class="container">
        <div>
          <router-link to="/">Главная</router-link>
        </div>
        <div>
          <router-link to="/about">О проекте</router-link>
        </div>
      </div>
    </header>
    <router-view />
  </div>
</template>

<style lang="scss">
.container {
  display: flex;
  div {
    flex: 1;
    border: 1px solid lightgray;
    text-align: center;
    height: 50px;
    font-size: 32px;
  }
}
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  margin: 0;
  padding: 0;

  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

header {
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #7e9ef5;
    }
  }
}
</style>
