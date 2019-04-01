import { fetch } from '../../utils/util'
//获取应用实例
var commonCityData = require('../../utils/city.js');
var app = getApp();
Page({
    data: {
        info: [],
        provinces: [],
        citys: [],
        districts: [],
        selProvince: '请选择',
        selCity: '请选择',
        selDistrict: '请选择',
        selProvinceIndex: 0,
        selCityIndex: 0,
        selDistrictIndex: 0
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id
		});
        this.initCityData(1);
    },
    onShow: function () {
        this.getInfo();
    },
    //初始化城市数据
    initCityData: function (level, obj) {
        if (level == 1) {
            var pinkArray = [];
            for (var i = 0; i < commonCityData.cityData.length; i++) {
                pinkArray.push(commonCityData.cityData[i].name);
            }
            this.setData({
                provinces: pinkArray
            });
        } else if (level == 2) {
            var pinkArray = [];
            var dataArray = obj.cityList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                citys: pinkArray
            });
        } else if (level == 3) {
            var pinkArray = [];
            var dataArray = obj.districtList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                districts: pinkArray
            });
        }
    },
    bindPickerProvinceChange: function (event) {
        var selIterm = commonCityData.cityData[event.detail.value];
        this.setData({
            selProvince: selIterm.name,
            selProvinceIndex: event.detail.value,
            selCity: '请选择',
            selCityIndex: 0,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(2, selIterm);
    },
    bindPickerCityChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[event.detail.value];
        this.setData({
            selCity: selIterm.name,
            selCityIndex: event.detail.value,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(3, selIterm);
    },
    bindPickerChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[event.detail.value];
        if (selIterm && selIterm.name && event.detail.value) {
            this.setData({
                selDistrict: selIterm.name,
                selDistrictIndex: event.detail.value
            })
        }
    },
    bindCancel: function () {
        wx.navigateBack({});
    },
    bindSave: function (e) {
        var that = this;
        var nickname = e.detail.value.nickname;
        var address = e.detail.value.address;
        var mobile = e.detail.value.mobile;

        if (nickname == "") {
            app.tip({content: '请填写联系人姓名~~'});
            return
        }
        if (mobile == "") {
            app.tip({content: '请填写手机号码~~'});
            return
        }
        if (this.data.selProvince == "请选择") {
            app.tip({content: '请选择地区~~'});
            return
        }
        if (this.data.selCity == "请选择") {
            app.tip({content: '请选择地区~~'});
            return
        }
        var city_id = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].id;
        var district_id;
        if (this.data.selDistrict == "请选择" || !this.data.selDistrict) {
            district_id = '';
        } else {
            district_id = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[this.data.selDistrictIndex].id;
        }
        if (address == "") {
            app.tip({content: '请填写详细地址~~'});
            return
        }
		let params = {
			id: that.data.id,
			province_id: commonCityData.cityData[this.data.selProvinceIndex].id,
			province_str: that.data.selProvince,
			city_id: city_id,
			city_str: that.data.selCity,
			district_id: district_id,
			district_str: that.data.selDistrict,
			nickname: nickname,
			address: address,
			mobile: mobile,
		}
		fetch('POST', '/my/address/set', params).then(res => {
			if (res.code != 200) {
				app.alert({"content": res.msg});
				return;
			}
			// 跳转
			wx.navigateBack({});
		})
    },
    deleteAddress: function (e) {
        let that = this;
        let params = {
            "content": "确定删除？",
            "cb_confirm": function () {
				fetch('POST', '/my/address/ops', {id: that.data.id, act:'del'}).then(res => {
					app.alert({"content": res.msg});
					if (res.code === 200) {
						// 跳转
						wx.navigateBack({});
					}
				})
            }
        };
        app.tip(params);
    },
    getInfo: function () {
        var that = this;
        if (that.data.id < 1) {
            return;
		}
		fetch('GET', '/my/address/info', {id: that.data.id}).then(res => {
			if (res.code != 200) {
				app.alert({"content": res.msg});
				return;
			}
			let info = resp.data.info;
			that.setData({
				info: info,
				selProvince: info.province_str ? info.province_str : "请选择",
				selCity: info.city_str ? info.city_str : "请选择",
				selDistrict: info.area_str ? info.area_str : "请选择"
			});
		})
    }
});
