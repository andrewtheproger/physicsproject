<template>
  <div class="hello">
    <h1>Вы авторизованы как {{ user === "user" ? "Пользователь" : "Админ"}}</h1>
    <form method="get">
      <div class="buttondiv">
        <input type="text" placeholder="Искать задачу по номеру..." />
        <br />
        <input type="submit" />
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    user: String
  }
};
</script>

<style scoped lang="scss">
.buttondiv {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  input {
    width: 100%
  }
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;

  li {
    display: inline-block;
    margin: 0 10px;
  }
}
a {
  color: #7e9ef5;
}
</style>
