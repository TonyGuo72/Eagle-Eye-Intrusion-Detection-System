Page({
  data:{
    inputUsername:"",
    inputPassword:""
  },

  usernameInput: function (e) {
    // console.log("输入的yonghuming值为："+e.detail.value);
    this.setData({
      inputUsername: e.detail.value
    })
  },

  passwordInput: function (e) {
    // console.log("输入mima的值为：" + e.detail.value);
    this.setData({
      inputPassword: e.detail.value
    })
  },

  login:function(e){
    console.log("输入的yonghuming值为：" + this.data.inputUsername);
    console.log("输入的mima值为：" + this.data.inputPassword);
    wx.request({
      url: 'http://127.0.0.1:5000/login', //获取服务器地址，此处为本地地址
      data: 
      {   //向服务器发送的信息
          username:this.data.inputUsername,
          password:this.data.inputPassword,
      },
      method: "POST",
      header:
      {
        "content-type": "application/x-www-form-urlencoded"   //使用POST方法要带上这个header
      },
      
      success (res) {
        if(res.data.code == 10000)
        {
          if(res.data.msg == "用户名不能为空")
          {
            wx.showToast({
              title: '用户名不能为空',
              icon: 'none',
              duration: 2000//持续的时间
            })
          }
          else if(res.data.msg == "密码不能为空")
          {
            wx.showToast({
              title: '密码不能为空',
              icon: 'none',
              duration: 2000//持续的时间
            })
          }
          else
          {
            wx.showToast({
              title: '用户名不存在或密码错误',
              icon: 'none',
              duration: 2000//持续的时间
            })
          }
        }
        else
        {
          console.log(res.data)
          wx.switchTab({
          url: '/pages/monitor/monitor',
        })
        }
      }
    })
  },

  register:function(){
    wx.redirectTo({
      url: '/pages/register/register',
    })
  }
})