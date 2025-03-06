<template>
    <div class="login-form">
        <h3>로그인</h3>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">아이디:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div class="form-group">
                <label for="password">비밀번호:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <div class="form-group">
                <button type="submit" class="btnL">로그인</button>
            </div>
        </form>
        <div class="">
            <!-- <router-link to="/login">회원가입</router-link> -->
            <a href="#">회원가입</a>
        </div>
    </div>
  </template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      // 로그인 처리 로직
      console.log("Username:", this.username);
      console.log("Password:", this.password);
    },
  },
}
</script>