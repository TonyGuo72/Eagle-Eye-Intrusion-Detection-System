Page({
  data:{
    inputUsername:"",
    inputPassword:"",
    inputEmail:"",
    inputID:"",
    inputVericode:"",
    reVericode:"",
  },

  usernameInput: function (e) {
    // console.log("输入的yonghuming值为："+e.detail.value);
    this.setData({
      inputUsername: e.detail.value,
    })
  },

  passwordInput: function (e) {
    // console.log("输入mima的值为：" + e.detail.value);
    this.setData({
      inputPassword: e.detail.value,
    })
  },

  idInput: function (e) {
    // console.log("输入id的值为：" + e.detail.value);
    this.setData({
      inputID: e.detail.value,
    })
  },

  emailInput: function (e) {
    // console.log("输入email的值为：" + e.detail.value);
    this.setData({
      inputEmail: e.detail.value,
    })
  },

  vericodeInput: function (e) {
    // console.log("输入yanzhengma的值为：" + e.detail.value);
    this.setData({
      inputVericode: e.detail.value,
    })
  },

  getVericode:function()
  {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/sendVericode', //获取服务器地址，此处为本地地址
      method: "POST",
      header:
      {
        "content-type": "application/x-www-form-urlencoded"   //使用POST方法要带上这个header
      },
      data: 
      {   //向服务器发送的信息
        username:this.data.inputUsername,
        password:this.data.inputPassword,
        id:this.data.inputID,
        email:this.data.inputEmail,     
      },
      success: (res) => {
        if(res.data.code == 10000)
        {
          wx.showToast({
            title: res.data.msg,
            icon: 'none',
            duration: 2000//持续的时间
          })
        }
        else{
          that.setData({
            reVericode:res.data.revericode,
          })
          console.log(that.data.reVericode)
          wx.showToast({
            title:'请及时查收',
            icon: 'none',
            duration: 2000//持续的时间
          })
        }
      },
    })
    
    
  },

  register:function(){
    console.log(this.data.reVericode);
    console.log(this.data.inputVericode);
    // if(this.data.inputVericode != "" && (this.data.reVericode == this.data.inputVericode))
    if((this.data.reVericode == this.data.inputVericode))
    {
      wx.request({
        url: 'http://127.0.0.1:5000/register', //获取服务器地址，此处为本地地址
        method: "POST",
        header:
        {
          "content-type": "application/x-www-form-urlencoded"   //使用POST方法要带上这个header
        },
        data: 
        {   //向服务器发送的信息
          username:this.data.inputUsername,
          password:this.data.inputPassword,
          id:this.data.inputID,
          email:this.data.inputEmail,
        },

        success: (res) => {
          if(res.data.code == 10000)
          {
            wx.showToast({
              title: res.data.msg,
              icon: 'none',
              duration: 2000//持续的时间
            })
          }
          else{
            console.log(res);
            wx.showToast({
              title: res.data.msg,
              icon: 'none',
              duration: 2000//持续的时间
            })
            wx.redirectTo({
              url: '/pages/index/index',
            })     
          }
        },
      })
    }
    else
    {
      wx.showToast({
        title: "验证码有误",
        icon: 'none',
        duration: 2000//持续的时间
      })
    }
    
    
  },

  return:function(){
    wx.redirectTo({
      url: '/pages/index/index',
    })
  }
})