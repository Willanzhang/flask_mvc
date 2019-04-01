import { fetch } from '../../utils/util'
//获取应用实例
var app = getApp();
Page({
    data: {
        list: []
    },
    onShow: function () {
        this.getList()
    },
    selectTap: function (e) {
        //从商品详情下单选择地址之后返回
        let params = {
            id: e.currentTarget.dataset.id,
            act: 'default'
        }
        fetch('POST', '/my/address/ops', params).then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
            }
            // this.setData({
            //     list: res.data.list
            // })
            wx.navigateBack({});
        })
    },
    addressSet: function (e) {
        wx.navigateTo({
            url: "/pages/my/addressSet?id=" + e.currentTarget.dataset.id
        })
    },
    getList() {
        fetch('GET', '/my/address/index').then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
            }
            this.setData({
                list: res.data.list
            })
        })
    }

});
