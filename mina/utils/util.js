const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

const fetch = (method, url, params) => {
  const lkey = wx.getStorageSync('lkey') || ''
  const sessionData = wx.getStorageSync('sessionData') || ''
  // const channelTag = wx.getStorageSync('channelTag') || '1'
  // const sendData = { channelType: '1', channelTag: '1', lkey: lkey, sessionData: sessionData ,...params}
  const sendData = { ...params }
  const data = getApp().globalData
  return new Promise((resolve, reject) => {
    wx.request({
      // url: data.extConfig.apiUrl + url,
      // url: 'https://localhost:5001' + url,
      // url: 'https://game.peralppay.com' + url,
      url: data.config.url + url,
      // url: 'https://api.66jingcai.cn' + url,
      data: sendData,
      header: {
        'Authorization': wx.getStorageSync('token') || '',
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: method,
      success(res) {
        if (res.statusCode === 401) {
          let tmp = getCurrentPages()
          let tmpArr = tmp[tmp.length - 1].__route__.split('/')
          let tmpStr = tmpArr[tmpArr.length - 1]
          wx.removeStorageSync('thirdSession')
          wx.reLaunch({ url: tmpStr })
          return
        } else if (res.statusCode === 404) {
          wx.showToast({
              title: '服务器繁忙',
              image: '/static/images/common/err.png',
              duration: 2000
            })
            return
        }
        if (res.statusCode != 200) {
          reject(res.data)
        } else if (res.statusCode = 200) {
          if ( typeof res.data === 'string') {
            wx.showToast({
              title: '服务器繁忙',
              image: '/static/images/common/err.png',
              duration: 2000
            })
            return
          }
          if (res.data.errCode) {
            wx.showToast({
              title: res.data.msg,
              image: '/static/images/common/err.png',
              duration: 2000
            })
            // wx.removeStorageSync('lkey')
            if (res.data.errCode === 3) { //未登录
              let shareParam = wx.getStorageSync('channelTag')
              console.log('99999')
              wx.clearStorage()
              let tmp = getCurrentPages()
              let tmpArr = tmp[tmp.length - 1].__route__.split('/')
              let tmpStr = tmpArr[tmpArr.length - 1]
              wx.reLaunch({ url: `/${tmp[tmp.length - 1].__route__}?shareParam=${shareParam}`})
              console.log('未登录',tmp[tmp.length - 1].__route__ )
            }
            reject(res.data)
            return false
          }
          resolve(res.data)
        }

      },
      fail(res) {
        console.log( data.config.url + url,'failt**-------', res)
        if (res.statusCode != 200) {
        }
        reject(res.data)
      }
    })
  })
}

const upload = (url, path, name, params) => {
  const data = getApp().globalData
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: data.extConfig.apiUrl + url,
      filePath: path,
      name: name,
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      formData: params, //可放入和服务器约定的token, 'session_token': wx.getStorageSync('session_token')
      success(res) {
        resolve(res)
      },
      fail(res) {
        reject(res)
      }
    })
  })
}

module.exports = {
  formatTime,
  fetch,
  upload
}
