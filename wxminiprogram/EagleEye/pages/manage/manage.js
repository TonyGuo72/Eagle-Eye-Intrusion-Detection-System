Page({
  data: {
    inputShowed: false,  
    listData:[
    ],
    infostring:""
  },

  onLoad: function () {
    var that = this;
    wx.request({
          url: 'http://127.0.0.1:5000/staff/list', //获取服务器地址，此处为本地地址
          data: 
          {   //向服务器发送的信息
          },
          method: "GET",
          dataType: 'json',
          
          success (res) {
            console.log(res);
            // that.setData({
            //   dataList: res.data.items
            // })
            that.setData({
              listData:res.data.items
            })     
          }
        })
  },

  showInput: function () {
    this.setData({
      inputShowed: true   //设置文本框可以输入内容
    });
  },
  // 取消搜索
  hideInput: function () {
    this.setData({
      inputShowed: false
    });
  },

  search: function () {

  },
  refresh : function()
  {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/staff/list', //获取服务器地址，此处为本地地址
      data: 
      {   //向服务器发送的信息
      },
      method: "GET",
      dataType: 'json',
      
      success (res) {
        console.log(res);
        // that.setData({
        //   dataList: res.data.items
        // })
        that.setData({
          listData:res.data.items
        })
        wx.showToast({
          title: '刷新成功',
          icon: 'none',
          duration: 2000//持续的时间
        })        
      }
    })
  },
 })
 