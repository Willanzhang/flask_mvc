//login.js
//获取应用实例
let app = getApp();
import { fetch } from '../../utils/util'
Page({
  data: {
    remind: '加载中',
    angle: 0,
    reFlag: true,
    userInfo: {}
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/food/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    })
    // this.login();
    this.checkLogin()
  },
  onShow:function(){

  },
  onReady: function(){
    let that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    console.log('123')
    wx.onAccelerometerChange(function(res) {
      let angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
  checkLogin: function() {
    let that = this
    wx.login({
      success(res) {
        if (res.code) {
          fetch("POST", '/member/check-reg', {code: res.code})
            .then(res => {
              if (res.code === 200) {
                that.setData({
                  reFlag: true
                },()=> {
                  app.setCache("token", res.data.token)
                  that.goToIndex()
                })
              } else {
                that.setData({
                  reFlag: false
                })
              }
            })
        } else {
          app.alert({'content': '登录失败，请重新点击~~'})
        }
      }
    })
  },
  login:function (e) {
    let that = this
    if(!e.detail.userInfo) {
      app.alert({'content': '登录失败，请重新点击~~'});
      return;
    }
    let data = e.detail.userInfo;
    wx.login({
      success(res) {
        if (res.code) {
          // 发起网络请求
          data['code'] = res.code
          fetch('POST', '/member/login', data).then(resp => {
            if (resp.data.code !== 200) {
              app.alert({'content': '登录失败，请重新点击~~'})
              return;
            } else {
              wx.setStorageSync({
                token: resp.data.data.token
              })
              app.setCache("token", resp.data.data.token)
              that.goToIndex()
            }
          })
        } else {
          app.alert({'content': '登录失败，请重新点击~~'})
        }
      }
    })
  }
});
