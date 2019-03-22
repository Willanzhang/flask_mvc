//index.js
//获取应用实例
import { fetch } from '../../utils/util'
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p: 1,
        processing: false
    },
    onLoad: function () {
        this.getPageInfo()
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    getPageInfo () {
        fetch('POST', '/food/index').then(res => {
            if(res.code === 200) {
                this.setData({
                    data: res.data
                })
                this.getFoodList()
            }
        })
    },
    getFoodList () {

        console.log(this.data.loadingMoreHidden)
        if(this.data.processing) {
            return
        }
        if(!this.data.loadingMoreHidden) {
            return
        }
        this.setData({
            processing: true
        })
        let params = {
            cat_id: this.data.activeCategoryId,
            mix_ky: this.data.searchInput,
            p: this.data.p
        }
        fetch('POST', '/food/search', params).then(res => {
            if (res.code === 200) {
                this.setData({
                    goods: this.data.goods.concat(res.data.list|| []),
                    P: ++this.data.p,
                    processing: false
                })
                if (res.data.has_more === 0) {
                    this.setData({
                        loadingMoreHidden: true
                    })
                }
            }
        })
    },
    catClick (e) {
        this.setData({
            activeCategoryId: e.currentTarget.id,
            loadingMoreHidden: true,
            goods: [],
            p: 1
        })
        this.getFoodList()
    },
    onReachBottom () {
        setTimeout(() => {
            this.getFoodList()
        }, 500);
    }
});
