<template>
  <Panel header="회원가입">
    <Form @submit="regist" class="flex justify-center flex-col gap-4">
      <Message v-if="errorMessage" severity="error" size="small" icon="pi pi-times-circle" class="mb-2">{{ errorMessage }}</Message>
      <div class="flex flex-col gap-1">
          <label for="userId">* 아이디</label>  
          <div class="flex gap-1">
            <InputText type="text" name="userId" v-model="userId" maxlength="20" @input="handleInput_id"/>
            <Button label="중복확인" severity="info" class="whitespace-nowrap" @click="idDuplicationCheck" />
          </div>
          <Message :severity="isIdValid? 'success' : 'error'" size="small" variant="simple">{{ message_id }}</Message>
      </div>
      <div class="flex flex-col gap-1">
          <label for="userId">* 비밀번호</label> 
          <div class="flex gap-1">
            <InputText type="password" name="password" v-model="password" maxlength="16" @input="filterInputs1('password')"/>
            <InputText type="password" name="password_re" v-model="password_re" maxlength="16" placeholder="비밀번호를 재입력하세요." @input="filterInputs1('password_re')"/>
          </div>
          <Message size="small" variant="simple">비밀번호는 영문, 숫자, 특수문자 조합으로 8~16자 이내여야 합니다.</Message>
      </div>
      <div class="flex flex-col gap-1">
          <label for="userId">* 이름</label> 
          <div class="flex gap-1">
            <InputText type="text" name="userName" v-model="userName" maxlength="15"/>
          </div>
      </div>
      <div class="flex flex-col gap-1">
          <label for="userId">* 사용자 권한</label> 
          <div class="flex flex-wrap gap-4">
            <div class="flex items-center gap-2">
                <RadioButton v-model="userRole" inputId="ROLE_USER" name="userRole" size="small" value="ROLE_USER" />
                <label for="ROLE_USER">일반 사용자</label>
            </div>
            <div class="flex items-center gap-2">
                <RadioButton v-model="userRole" inputId="ROLE_ADMIN" name="userRole" size="small" value="ROLE_ADMIN" />
                <label for="ROLE_ADMIN">관리자</label>
            </div>
        </div>
      </div>
      <Button type="submit" severity="success" label="회원가입" />
    </Form>
    <router-link to="/login" class="flex flex-col gap-1"><Button label="로그인" variant="link" /></router-link>
  </Panel>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  name: 'Regist',
  data() {
    return {
        userId: "",
        password: "",
        password_re: "",
        userName: "",
        userRole: "ROLE_USER",
        errorMessage: "",
        isIdValid: false,
        message_id: "",
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
      if (!this.password_re.trim()) {
        this.errorMessage = "비밀번호를 재입력해주세요.";
        return false;
      }
      if (!this.userName.trim()) {
        this.errorMessage = "이름을 입력해주세요.";
        return false;
      }
      if (!this.userRole) {
        this.errorMessage = "사용자 권한을 선택해주세요.";
        return false;
      }
      return true;
    },
    // 비밀번호 형식 검사
    passwordCheck() {
      const pwRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,16}$/;

      if (!pwRegex.test(this.password)) {
        this.errorMessage = "비밀번호는 영문, 숫자, 특수문자 조합으로 8~16자 이내여야 합니다.";
        return false;
      }

      if (!this.password_re || this.password_re !== this.password) {
        this.errorMessage = "비밀번호가 일치하지 않습니다.";
        return false;
      }

      return true;
    },
    // 아이디 중복 검사
    async idDuplicationCheck() {
      if (!this.userId.trim()) {
        this.errorMessage = "아이디를 입력해주세요.";
        return;
      }

      try {
        // 로그인 API 요청
        const response = await axios.get("http://localhost:8081/api/auth/regist/idCheck", {
          params: { userId: this.userId },
        });

        // 유효한 아이디 여부 반환
        this.isIdValid = response.data.result;
        this.message_id = response.data.message;
      } catch (error) {
        this.errorMessage = error.response.data.message;
      }
    },
    handleInput_id(event) {
      this.isIdValid = false;
      this.message_id = "";
      this.filterInputs1('userId');
    },
    async regist() {
      if(!this.basicCheck()) {
        return;
      }

      if(!this.isIdValid) {
        this.errorMessage = "아이디 중복확인을 진행해주세요.";
        return;
      }

      if(!this.passwordCheck()) {
        return;
      }

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