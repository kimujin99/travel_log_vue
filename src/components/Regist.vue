<template>
  <Panel header="회원가입">
    <form @submit.prevent="regist">
      <div class="flex flex-col gap-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="value" />
      </div>
      <div class="flex flex-col gap-2">
          <label for="username">Username</label>
          <InputText id="username" v-model="value" />
      </div>
    </form>

          <!-- <div class="form-group">
              <label for="userId">* 아이디:</label>
              <input type="text" id="userId" class="inputM" v-model="userId" required maxlength="20" @input="idCheck"/>
              <input type="button" class="btnS btn-blue" value="중복확인" @click="idDuplicationCheck"/>
          </div>
          <div class="form-group">
              <div v-if="message_id" :class="{'valid': isIdValid, 'invalid': !isIdValid}"><p>{{ message_id }}</p></div>
          </div>
          <div class="form-group">
              <label for="password">* 비밀번호:</label>
              <input type="password" id="password" class="inputM" v-model="password" required maxlength="16" @input="passwordCheck" />
              <input type="password" id="password_re" class="inputM" v-model="password_re" placeholder="비밀번호를 재입력하세요." required maxlength="16" @input="passwordCheck" />
          </div>
          <div class="form-group">
              <div v-if="message_pw" :class="{'valid': isPwValid, 'invalid': !isPwValid}"><p>{{ message_pw }}</p></div>
          </div>
          <div class="form-group">
              <label for="user_role">* 이름:</label>
              <input type="text" id="user_role" class="inputM" v-model="userName" required maxlength="15"/>
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
          </div> -->
      <div class="">
          <router-link to="/login">로그인</router-link>
      </div>
  </Panel>
</template>

<script>
import axios from "axios";
import InputText from 'primevue/inputtext';
import Panel from 'primevue/panel';
import Message from 'primevue/message';

export default {
  name: 'Regist',
  components: {
    InputText,
    Panel,
    Message,
  },
  data() {
    return {
        userId: "",
        password: "",
        password_re: "",
        userName: "",
        userRole: "ROLE_USER",
        errorMessage: "",
        isIdValid: false,
        message_id: "아이디 중복확인을 진행해주세요.",
        isPwValid: false,
        message_pw: "비밀번호를 입력해주세요.",
    };
  },
  methods: {
    // 비밀번호 형식 검사
    passwordCheck() {
      const pwRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,16}$/;

      if(!this.password) {
        this.isPwValid = false;
        this.message_pw = "비밀번호를 입력해주세요.";
        return;
      }

      if (!pwRegex.test(this.password)) {
        this.isPwValid = false;
        this.message_pw = "비밀번호는 영문, 숫자, 특수문자 조합으로 8~16자 이내여야 합니다.";
        return;
      }

      if (!this.password_re || this.password_re !== this.password) {
        this.isPwValid = false;
        this.message_pw = "비밀번호가 일치하지 않습니다.";
        return;
      }

      this.isPwValid = true;
      this.message_pw = "유효한 비밀번호입니다.";
    },
    // 아이디 형식 검사
    idCheck() {
      this.isIdValid = false;
      this.message_id = "아이디 중복확인을 진행해주세요.";
      this.userId = this.userId.replace(/[^A-Za-z\d!@#$%^&*]/g, "");
      if (this.userId.length > 20) {
        this.userId = this.userId.slice(0, 20);
      }
    },
    // 아이디 중복 검사
    async idDuplicationCheck() {
      // 인풋에 값이 있는지 확인
      if (!this.userId.trim()) {
        this.message_id = "아이디를 입력해주세요.";
        return;
      }

      try {
        // 로그인 API 요청
        const response = await axios.get("http://localhost:8081/api/auth/regist/idCheck", {
          params: { userId: this.userId },
        });

        // 유효한 아이디 여부 반환환
        this.isIdValid = response.data.result;
        this.message_id = response.data.message;
      } catch (error) {
        this.errorMessage = error.response.data.message;
      }
    },
    async regist() {
      try {
        // 로그인 API 요청
        const response = await axios.post("http://localhost:8081/api/auth/regist", {
            userId: this.userId,
            password: this.password,
            userName: this.userName,
            userRole: this.userRole,
        });

        alert("회원가입 완료되었습니다.");

        // 로그인 성공 후 원하는 페이지로 이동
        this.$router.push("/login");
      } catch (error) {
        // 오류 처리
        console.log("ERROR_STATUS : " + error.status);
        this.errorMessage = error.response.data.message;
      }
    }
  },
}
</script>