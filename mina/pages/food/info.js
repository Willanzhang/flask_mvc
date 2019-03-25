//index.js
import { fetch } from '../../utils/util'
import { getCurrentPageUrlWithArgs } from '../../utils/common'
//获取应用实例
let app = getApp();
let WxParse = require('../../wxParse/wxParse.js');

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount:2
    },
    onLoad: function (options) {
        var that = this;
        this.getInfo(options.id);
        that.setData({
            id: options.id,
            commentList: [
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                },
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                }
            ]
        });

        // WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
    },
    onShareAppMessage () {
        return {
            title: this.data.info.name,
            path: `/page/food/info?id=${this.data.id}`,
            success: function(res) {
                // 成功
                console.log('成功')
                let params = {
                    url: getCurrentPageUrlWithArgs()
                }
                fetch('POST', '/member/share', params)
            },
            fail: function() {
                // 失敗
                console.log('轉發失敗')
            }
        }
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
        
        console.log(x)
        var x= 1

    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {

    },
    buyNow: function () {
        wx.navigateTo({
            url: "/pages/order/index"
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getInfo (id) {
        let params = {
            id
        }
        fetch('POST', '/food/info', params).then(res => {
            console.log(res)
            if (res.code === 200) {
                this.setData({
                    info: res.data.info,
                    buyNumMax: res.data.info.stock
                })
                WxParse.wxParse('article', 'html', this.data.info.summary, this, 5)
            } else {
                app.alert(res.data.msg)
            }
        })
    }
});
