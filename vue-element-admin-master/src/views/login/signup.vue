<template>
  <div class="login-container">
    <el-form ref="signupForm" :model="signupForm" :rules="signupRules" class="login-form"  label-position="left">

      <div class="title-container">
        <h3 class="title">注册</h3>
      </div>

      <el-form-item label="用户名" prop="username">
        <el-input
          @input="e=>signupForm.username=validSe(e,255)"
          class="text-input"
          ref="username"
          v-model="signupForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
        />
      </el-form-item>

      <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
        <el-form-item label="密码" prop="password">
          <el-input
            @input="e=>signupForm.password=validSe(e,255)"
            class="text-input"
            :key="passwordType"
            ref="password"
            v-model="signupForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
          />
        </el-form-item>
      </el-tooltip>

      <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
        <el-form-item label="确认密码" prop="true_password">
          <el-input
            @input="e=>signupForm.true_password=validSe(e,255)"
            class="text-input"
            :key="passwordType"
            ref="true_password"
            v-model="signupForm.true_password"
            :type="passwordType"
            placeholder="重复密码"
            name="true_password"
            tabindex="3"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
          />
        </el-form-item>
      </el-tooltip>

      <el-form-item label="ID" prop="realname">
        <el-input
          @input="e=>signupForm.id=validSe(e,15)"
          class="text-input"
          ref="id"
          v-model="signupForm.id"
          placeholder="员工ID"
          name="id"
          type="text"
          tabindex="4"
        />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input
          class="text-input"
          style="width: 250px"
          ref="email"
          v-model="signupForm.email"
          placeholder="邮箱"
          name="email"
          type="email"
          tabindex="5"
        />
        <el-button @click="handleEmail"
                   :disabled="disabled=!showtime">
          获取验证码
        </el-button>
      </el-form-item>

      <el-form-item label="验证码" prop="verification">
        <el-input
          class="text-input"
          ref="verification"
          v-model="signupForm.verification"
          placeholder="验证码"
          name="verification"
          type="text"
          tabindex="6"
        />
      </el-form-item>
      <el-form-item
        style="padding-left: 140px;
        border: 0px solid rgba(0,0,0,100);
        background: rgba(45,58,75,100);
        border-radius: 5px;">
        <el-button @click="handleCancel">取 消</el-button>
        <el-button type="primary" @click="handleSend">确 定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

import { sendEmail, signup } from '@/api/user'

export default {
  name: 'signup',
  data() {
    const validataTruePassword = (rule, value, callback) => {
      if (value !== this.signupForm.password) {
        callback(new Error('两次输入不一致'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      let mailReg
      mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      /*if (!value) {
        return callback(new Error('邮箱不能为空'))
      }*/
      if (mailReg.test(value)) {
        callback()
      } else {
        callback(new Error('请输入正确的邮箱格式'))
      }
    }
    return {
      centerDialogVisible: false,
      signupForm: {
        username: '',
        password: '',
        true_password: '',
        id: '',
        email: '',
        verification: ''
      },
      showtime:true,
      count:'',
      timer:null,
      signupRules: {
        username: [{ trigger: 'blur' }],
        password: [{ trigger: 'change', validator: validatePassword }],
        true_password: [{ trigger: 'change', validator: validataTruePassword }],
        email: [{ trigger: 'change', validator: validateEmail }]
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  methods: {
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    },
    handleCancel(){
      this.loading = true
      this.$router.push({ path:'/login'})
      this.loading = false
    },
    handleEmail(){
      this.loading = true
      sendEmail({'email':this.signupForm.email}).then(response => {

        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleSend() {
      console.log(this.signupForm)
      if(this.signupForm.username===''||this.signupForm.password===''||this.signupForm.id===''||this.signupForm.email===''||this.signupForm.true_password===''||this.signupForm.verification===''){
        this.$notify({
          title: 'fail',
          message: '还有没填的选项！',
          type: 'error',
          duration: 2000
        })
      }else if (this.signupForm.password!==this.signupForm.true_password){
        this.$notify({
          title: 'fail',
          message: '两次密码不一致！',
          type: 'error',
          duration: 2000
        })
      }else{
        this.loading = true
        let that=this
        signup(this.signupForm).then(response => {
          console.log(response)
          that.$notify({
            title: 'Success',
            message: '注册成功！',
            type: 'success',
            duration: 2000
          })
          this.$router.push({ path: '/', query: this.otherQuery })
          this.loading = false
        }).catch(() => {
          that.$notify({
            title: 'faild',
            message: '注册失败！',
            type: 'error',
            duration: 2000
          })
          this.loading = false
        })
      }
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}

</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
    .el-form-item__label{
      color: white;
      padding-top: 5px;
      padding-left: 5px;
      width: 85px;
    }
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 100px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .text-input{
    width:350px;
    padding-right: 5px;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
