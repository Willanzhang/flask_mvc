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
        shopCarNum: 0,
        commentCount:2
    },
    onLoad: function (options) {
        this.setData({
            id: options.id
        });

        // WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
    },
    onShow:function(){
        this.getInfo(this.data.id);
        this.getComments();
    },
    onShareAppMessage () {
        let params = {
            url: getCurrentPageUrlWithArgs()
        }
        console.log(params, '123')
        fetch('POST', '/member/share', params)
        return {
            title: this.data.info.name,
            path: `/page/food/info?id=${this.data.id}`,
            success: function(res) {
                // 成功
                console.log('成功')
                
            },
            fail: function() {
                // 失敗
                console.log('轉發失敗')
            }
        }
    },
    getComments () {
        let params = {
            id: this.data.id
        }
        fetch('GET', '/food/comments', params).then(res => {
            if(res === 200) {
                this.setData({
                    commentList: resp.data.list,
                    commentCount: resp.data.count,
                })
            }
            // app.alert({
            //     content: res.msg
            // })
        })
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
        let params = {
            id: this.data.info.id,
            number: this.data.buyNumber
        }
        fetch('POST', '/cart/set', params).then(res => {
            if(res === 200) {
                this.setData({
                    hideShopPopup: true
                })
            }
            app.alert({
                content: res.msg
            })
        })
    },
    buyNow: function () {
        let data = {
            goods: [{
                id: this.data.info.id,
                price: this.data.info.price,
                number: this.data.buyNumber,
            }]
        }
        this.setData({
            hideShopPopup: true
        })
        wx.navigateTo({
            url: "/pages/order/index?data=" + JSON.stringify(data)
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
                    buyNumMax: res.data.info.stock,
                    shopCarNum: res.data.cart_number
                })
                WxParse.wxParse('article', 'html', this.data.info.summary, this, 5)
            } else {
                app.alert({
                    content: res.msg
                })
            }
        })
    }
});
