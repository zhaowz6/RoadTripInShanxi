<template>
  <el-container class="container">
    <el-aside class="aside" width="200px" >
      <el-menu :default-active="activeIndex" active-text-color="#BAA7FFFF"	class="el-menu-vertical">
<!--        可视化分析-->
        <el-menu-item index="/dashboard" @click="navigateTo('/dashboard')">可视化页面</el-menu-item>
        <el-menu-item index="/users" @click="navigateTo('/users')">景区路线规划</el-menu-item>
        <!-- 其他菜单项 -->
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="logo">山西景区数据分析可视化</div>
      </el-header>

      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </el-container>

  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '/dashboard'
    };
  },
  methods: {
    navigateTo(path) {
      console.log(this.activeIndex);
      if (this.$route.path !== path) {
        this.activeIndex = path;
        this.$router.push(path);
      }
    }
  }
};
</script>

<style scoped>

.aside{
  background-color: #545c64;;
}
.container{
  height: 100vh;
  border: 1px solid #eee;
}

.header {
  background-color: #ffffff;
  text-align: center;
  line-height: 60px;
  border-bottom: 1px solid #ebeef5;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.main {
  padding: 20px;
}
</style>

