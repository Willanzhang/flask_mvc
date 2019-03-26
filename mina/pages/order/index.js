//获取应用实例
import { fetch } from '../../utils/util'
let app = getApp();
Page({
    data: {
        goods_list: [],
        default_address: {},
        yun_price: "",
        pay_price: "",
        total_price: "",
        params: null
    },
    onShow: function () {
        var that = this;
        this.getOrderInfo()

    },
    onLoad: function (e) {
        this.setData({
            data: JSON.parse(e.data)
        })
    },
    createOrder: function (e) {
        let params = {
            type: this.data.data.type,
            goods: JSON.stringify(this.data.data.goods)
        }
        fetch('POST', '/order/create', params).then(res => {
            wx.hideLoading()
            if (res.code !== 200) {
                app.alert({
                    content: res.msg
                })
                return
            }
            wx.navigateTo({
                url: "/pages/my/order_list"
            });
        })
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    getOrderInfo() {
        let params = {
            type: this.data.data.type,
            goods: JSON.stringify(this.data.data.goods)
        }
        
        fetch('POST', '/order/info', params).then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
                return;
            }
            this.setData({
                goods_list: res.data.food_list,
                default_address: res.data.default_address,
                yun_price: res.data.yun_price,
                pay_price: res.data.pay_price,
                total_price: res.data.total_price,
            })
        })
    }

});
