import { fetch } from '../../utils/util'
var app = getApp();
Page({
    data: {
        order_list:[],
        statusType: ["待付款", "待发货", "待确认", "待评价", "已完成","已关闭"],
        status:[ "-8","-7","-6","-5","1","0" ],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.setData({
            currentType: curType
        });
        this.getPayOrder();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info?order_sn=" + e.currentTarget.dataset.id
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
    },
    onShow: function () {
        this.getPayOrder();
    },
    orderCancel:function( e ){
        this.orderOps( e.currentTarget.dataset.id,"cancel","确定取消订单？" );
    },
    getPayOrder () {
        let params = {
            status: this.data.status[this.data.currentType]
        }
        fetch('POST', '/my/order', params).then(res => {
            if(res.code !== 200) {
                app.alert({
                    content: res.msg
                })
                return;
            }
            this.setData({
                order_list: res.data.pay_order_list
            })
        })
    },
    toPay:function( e ){
        var that = this;
        let params = {
            order_sn: e.currentTarget.dataset.id
        }
        fetch('POST', '/order/pay', params).then(res => {
            let resp = res.data;
            if (resp.code != 200) {
                app.alert({"content": resp.msg});
                return;
            }
            let pay_info = resp.data.pay_info;
            wx.requestPayment({
                'timeStamp': pay_info.timeStamp,
                'nonceStr': pay_info.nonceStr,
                'package': pay_info.package,
                'signType': 'MD5',
                'paySign': pay_info.paySign,
                'success': function (res) {
                },
                'fail': function (res) {
                }
            });
        })
    },
    orderConfirm:function( e ){
        this.orderOps( e.currentTarget.dataset.id,"confirm","确定收到？" );
    },
    orderComment:function( e ){
        wx.navigateTo({
            url: "/pages/my/comment?order_sn=" + e.currentTarget.dataset.id
        });
    },
    orderOps:function(order_sn,act,msg){
        let that = this;
        let params = {
            "content":msg,
            "cb_confirm":function(){
                let params = {
                    order_sn: order_sn,
                    act:act
                }
                fetch('POST', '/order/ops', params).then(res => {
                    var resp = res.data;
                    app.alert({"content": resp.msg});
                    if ( resp.code == 200) {
                        that.getPayOrder();
                    }
                })
            }
        };
        app.tip( params );
    }
});
