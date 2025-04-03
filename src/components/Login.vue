<template>
  <Panel style="width: 20rem;" header="로그인">
    <Form @submit="login" class="flex justify-center flex-col gap-4">
      <Message v-if="errorMessage" severity="error" size="small" icon="pi pi-times-circle" class="mb-2">{{ errorMessage }}</Message>
      <div class="flex flex-col gap-1">
          <InputText type="text" name="userId" v-model="userId" placeholder="아이디" maxlength="20" @input="filterInputs1('userId')"/>
      </div>
      <div class="flex flex-col gap-1">
          <InputText type="password" name="password" v-model="password" placeholder="비밀번호" maxlength="16" @input="filterInputs1('password')"/>
      </div>
      <Button type="submit" severity="success" label="로그인" />
    </Form>
    <router-link to="/regist" class="flex flex-col gap-1"><Button label="회원가입" variant="link" /></router-link>
  </Panel>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  name: 'Login',
  data() {
    return {
      userId: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    // 영어 대소문자, 숫자, !@#_ 특수문자 허용
    filterInputs1(field) {
      nextTick(() => {
        this[field] = this[field].replace(/[^A-Za-z\d!@#$_]/g, ""); 
      });
    },
    // 기본 형식 검사
    basicCheck() {
      if (!this.userId.trim()) {
        this.errorMessage = "아이디를 입력해주세요.";
        return false;
      }
      if (!this.password.trim()) {
        this.errorMessage = "비밀번호를 입력해주세요.";
        return false;
      }
      return true;
    },
    async login() {
      if(!this.basicCheck()) {
        return;
      }

      try {
        // 로그인 API 요청
        const response = await axios.post("http://localhost:8081/api/auth/login", {
          userId: this.userId,
          password: this.password,
        });

        // JWT 토큰 받아서 로컬 스토리지에 저장
        const token = response.data.token;
        const username = response.data.userName;
        const userId = response.data.userId;
        localStorage.setItem("authToken", token);
        localStorage.setItem("username", username);
        localStorage.setItem("userId", userId);

        // 헤더 업데이트 트리거
        window.dispatchEvent(new Event("storage"));

        this.$router.push("/");
      } catch (error) {
        // 오류 처리
        console.log("🔥 ERROR_STATUS : ", error.response?.status);
        console.log("🔥 ERROR_DATA : ", error.response?.data);
        console.log("🔥 ERROR_MESSAGE : ", error.message);
        this.errorMessage = error.response.data.message;
      }
    }
  },
}
</script>