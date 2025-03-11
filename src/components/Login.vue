<template>
    <div class="login-form">
        <h3>로그인</h3>
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="username">아이디:</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="form-group">
            <label for="password">비밀번호:</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <div class="form-group">
            <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
          </div>
            <div class="form-group">
                <button type="submit" class="btnL">로그인</button>
            </div>
        </form>
        <div class="">
            <router-link to="/regist">회원가입</router-link>
        </div>
    </div>
  </template>

<script>
import axios from "axios";

export default {
  name: 'Login',
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        // 로그인 API 요청
        const response = await axios.post("http://localhost:8081/api/auth/login", {
          username: this.username,
          password: this.password,
        });

        // JWT 토큰 받아서 로컬 스토리지에 저장
        const token = response.data.token;
        localStorage.setItem("authToken", token);

        // 로그인 성공 후 원하는 페이지로 이동 (예: 대시보드)
        this.$router.push("/main");
      } catch (error) {
        // 오류 처리
        console.log("ERROR_STATUS : " + error.status);
        this.errorMessage = error.response.data.message;
      }
    }
  },
}
</script>