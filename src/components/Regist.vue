<template>
    <div class="regist-form">
        <h3>회원가입</h3>
        <form @submit.prevent="regist">
            <div class="form-group">
                <label for="username">* 아이디:</label>
                <input type="text" id="username" class="inputM" v-model="userId" required />
                <input type="button" class="btnS btn-blue" value="중복확인"/>
            </div>
            <div class="form-group">
                <label for="password">* 비밀번호:</label>
                <input type="password" id="password" class="inputM" required />
                <input type="password" id="password_re" class="inputM" placeholder="비밀번호를 재입력하세요." v-model="password" required />
            </div>
            <div class="form-group">
                <label for="user_role">* 이름:</label>
                <input type="text" id="user_role" class="inputM" v-model="userName" required />
            </div>
            <div class="form-group">
                <label>* 사용자 권한:</label>
                <div class="radio-group">
                    <label class="radio-option">
                    <input type="radio" name="user_role" v-model="userRole" value="ROLE_USER" checked/>
                    <span class="custom-radio"></span>
                    일반 사용자
                    </label>

                    <label class="radio-option">
                    <input type="radio" name="user_role" v-model="userRole" value="ROLE_ADMIN" />
                    <span class="custom-radio"></span>
                    관리자
                    </label>
                </div>
            </div>
            <div class="form-group">
                <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
            </div>
            <div class="form-group">
                <button type="submit" class="btnL">회원가입</button>
            </div>
        </form>
        <div class="">
            <router-link to="/login">로그인</router-link>
        </div>
    </div>
  </template>

<script>
import axios from "axios";

// 아이디 중복 체크
let isIdValid = false;

// 비밀번호 유효성 체크
let isPwValid = false;

export default {
  name: 'Regist',
  data() {
    return {
        userId: "",
        password: "",
        userName: "",
        userRole: "",
        errorMessage: "",
    };
  },
  methods: {
    async regist() {
      try {
        // 로그인 API 요청
        const response = await axios.post("http://localhost:8081/api/auth/regist", {
            userId: this.userId,
            password: this.password,
            userName: this.userName,
            userRole: this.userRole,
        });

        // JWT 토큰 받아서 로컬 스토리지에 저장
        const token = response.data.token;
        localStorage.setItem("authToken", token);

        // 로그인 성공 후 원하는 페이지로 이동
        this.$router.push("/login");
      } catch (error) {
        // 오류 처리
        console.log(error);
        this.errorMessage = error.response.data.token;
      }
    }
  },
}
</script>