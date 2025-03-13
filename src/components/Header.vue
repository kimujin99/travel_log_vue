<template>
  <header>
    <div class="header-container">
      <div class="row-container">
        <span class="material-symbols-outlined mr8" style="font-size: 36px;">
          flight_takeoff
        </span>
        <h2>
          Travle Log
        </h2>
      </div>
      <div class="row-container">
        <p v-if="!isLoggedIn" class="mr8">
          <router-link to="/login" class="p-anchor">로그인</router-link>
        </p>
        <p v-if="!isLoggedIn">
          <router-link to="/regist" class="p-anchor">회원가입</router-link>
        </p>
        <p v-if="isLoggedIn" class="mr16">
          <span> {{ username }}님, 안녕하세요!</span>
        </p>
        <p v-if="isLoggedIn" class="mr8">
          <router-link to="/mypage" class="p-anchor">마이페이지</router-link>
        </p>
        <p v-if="isLoggedIn" class="p-anchor" @click="logout">
          로그아웃
        </p>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      token: localStorage.getItem("authToken"),
      username: localStorage.getItem("username"),
    };
  },
  computed: {
    isLoggedIn() {
      return !!this.token;
    }
  },
  created() {
    window.addEventListener("storage", this.syncLoginState);
  },
  beforeUnmount() {
    window.removeEventListener("storage", this.syncLoginState);
  }, 
  methods: {
    // localStorage 변경 감지
    syncLoginState() {
      this.token = localStorage.getItem("authToken");
      this.username = localStorage.getItem("username");
    },
    logout() {
      localStorage.removeItem("authToken");
      window.dispatchEvent(new Event("storage"));
      this.$router.push("/");
    }
  },
}
</script>