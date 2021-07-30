Page({
  data: {
      winWidth: 0,
      winHeight: 0,
      currentTab: 0,
      listData:[
    ],
  },
  onLoad: function() {

    //获取入侵记录表
      var that = this;
      wx.request({
        url: 'http://127.0.0.1:5000/staff/intrusion_records', //获取服务器地址，此处为本地地址
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

    

      /**
       * 获取当前设备的宽高
       */
      wx.getSystemInfo( {

          success: function( res ) {
              that.setData( {
                  winWidth: res.windowWidth,
                  winHeight: res.windowHeight
              });
          }

      });
  },
    
//  tab切换逻辑
  swichNav: function( e ) {

      var that = this;

      if( this.data.currentTab === e.target.dataset.current ) {
          return false;
      } else {
          that.setData( {
              currentTab: e.target.dataset.current
          })
      }
  },

  bindChange: function( e ) {

      var that = this;
      that.setData( { currentTab: e.detail.current });

  },

  refresh : function()
  {
    var that = this;
    wx.request({
      url: 'http://127.0.0.1:5000/staff/intrusion_records', //获取服务器地址，此处为本地地址
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