//获取应用实例
import { fetch } from '../../utils/util'
var app = getApp();
Page({
    data: {},
    onLoad() {

    },
    onShow() {
        let that = this;
        that.setData({
            user_info: {
                nickname: "编程浪子",
                avatar_url: "/images/more/logo.png"
            },
        })
        this.getInfo()
    },
    getInfo() {
        fetch('GET', '/member/info').then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
                return
            }
            this.setData({
                user_info: res.data.info
            })
        })
    }
});