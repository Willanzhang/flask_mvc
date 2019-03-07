const isDev = false
// 开发环境
// url: 'https://apidev.66jingcai.cn' + url,
// 线上
// url: 'https://api.66jingcai.cn' + url,
// appid: 'wx02c26262450039c7', // 线上环境
// appid: 'wx40a31196b8c2aedc', // 开发测试环境

// https://h5dev.66jingcai.cn	 // 内嵌webview 开发环境
// https://m.66jingcai.cn  // 内嵌webview 线上环境
let config = {}
if(isDev) {
  config = {
    appid: 'wxe3445334e3277c73',
    webView: 'https://h5dev.66jingcai.cn',
    url: 'http://127.0.0.1/api'
  }
} else {
  config = {
    appid: 'wxe3445334e3277c73',
    webView: 'https://m.66jingcai.cn',
    url: 'http://127.0.0.1/api'
  }
}
module.exports = config