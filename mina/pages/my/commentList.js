import { fetch } from '../../utils/util'
var app = getApp();
Page({
    data: {
        list: []
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onShow: function () {
        this.getList()
    },
    getList() {
        fetch('GET', '/my/comment/list').then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
                return
            }
            this.setData({
                list: res.data.list
            })
        })
    }
});
