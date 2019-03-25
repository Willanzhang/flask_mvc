let add = (arg1, arg2) => {
  let r1
  let r2
  let m
  let c
  try {
    r1 = arg1.toString().split('.')[1].length
  } catch (e) {
    r1 = 0
  }
  try {
    r2 = arg2.toString().split('.')[1].length
  } catch (e) {
    r2 = 0
  }
  c = Math.abs(r1 - r2)
  m = Math.pow(10, Math.max(r1, r2))
  if (c > 0) {
    let cm = Math.pow(10, c)
    if (r1 > r2) {
      arg1 = Number(arg1.toString().replace('.', ''))
      arg2 = Number(arg2.toString().replace('.', '')) * cm
    } else {
      arg1 = Number(arg1.toString().replace('.', '')) * cm
      arg2 = Number(arg2.toString().replace('.', ''))
    }
  } else {
    arg1 = Number(arg1.toString().replace('.', ''))
    arg2 = Number(arg2.toString().replace('.', ''))
  }
  return (arg1 + arg2) / m
}

let sub = (arg1, arg2) => {
  let r1
  let r2
  let m
  let n
  try {
    r1 = arg1.toString().split('.')[1].length
  } catch (e) {
    r1 = 0
  }
  try {
    r2 = arg2.toString().split('.')[1].length
  } catch (e) {
    r2 = 0
  }
  m = Math.pow(10, Math.max(r1, r2))
  n = (r1 >= r2) ? r1 : r2
  return Number(((arg1 * m - arg2 * m) / m).toFixed(n))
}

let mul = (arg1, arg2) => {
  let m = 0
  let s1 = arg1.toString()
  let s2 = arg2.toString()
  try {
    m += s1.split('.')[1].length
  } catch (e) { }
  try {
    m += s2.split('.')[1].length
  } catch (e) { }
  return Number(s1.replace('.', '')) * Number(s2.replace('.', '')) / Math.pow(10, m)
}

let div = (arg1, arg2) => {
  let t1 = 0
  let t2 = 0
  let r1
  let r2
  try {
    t1 = arg1.toString().split('.')[1].length
  } catch (e) { }
  try {
    t2 = arg2.toString().split('.')[1].length
  } catch (e) { }
  r1 = Number(arg1.toString().replace('.', ''))
  r2 = Number(arg2.toString().replace('.', ''))
  return (r1 / r2) * Math.pow(10, t2 - t1)
}

let checkPhone = (data) => {
  return /^(1[3|4|5|7|8][\d]{9}|0[\d]{2,3}-[\d]{7,8})$/.test(data)
}

/**
 * 价格过滤器，元为单位
 */
let filterPrice = (price) => {
  return Math.abs(price) / 100
}
/**
 * 时间格式化
 * 参数说明：timeStamp：时间戳（秒）fmt： 日期格式 yyyy:MM:dd hh:mm
*/
const format = (timeStamp, fmt) => {
  let date = new Date(timeStamp * 1000)
  let o = {
    "M+": date.getMonth() + 1, // 月份
    "d+": date.getDate(), // 日
    "h+": date.getHours(), // 小时
    "m+": date.getMinutes(), // 分
    "s+": date.getSeconds(), // 秒
    "q+": Math.floor((date.getMonth() + 3) / 3), // 季度
    "S": date.getMilliseconds() // 毫秒
  };
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
  }
  for (let k in o) {
    if (new RegExp("(" + k + ")").test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    }
  }
  return fmt;
}

const imgProcess = (url, width, height) => {
  if (!url.match(/static\/images\/customPage/)) {
    let temp = url.split(/.(jpg|png|gif)/ig)
    return temp[0] + '_' + width + '_' + height + '.' + temp[1]
  } else {
    return url
  }
}

const getNow = (useTime) => { // 获取的是否是今天...
  // console.log(useTime)
  let uTime = parseInt(useTime) * 1000
  let nowTime = new Date()
  let chineaseData = ''
  // let mistiming = Math.abs(uTime - nowTime)
  let mistiming = uTime - nowTime
  let day = new Date(uTime).getDate() - nowTime.getDate()
  if (mistiming > 259200000) {
    console.log('get now')
    chineaseData = format(useTime, 'MM月dd日')
  } else if (mistiming < 0 && mistiming > 90*60*100) { // 一场比赛的时间
      chineaseData = '今天'
  } else {
    switch (day) {
      case 0:
        chineaseData = '今天'
        break
      case 1:
        chineaseData = '明天'
        break;
      case 2:
        chineaseData = '后天'
        break;
      default:
        chineaseData = ''
        break;
    }
  }
  return chineaseData
}

// 计算地球上两点之间的距离 已经两点的经纬度 单位为度
const calcDistance = (lat1, lng1, lat2, lng2) => {
  var radLat1 = lat1 * Math.PI / 180.0;
  var radLat2 = lat2 * Math.PI / 180.0;
  var a = radLat1 - radLat2;
  var b = lng1 * Math.PI / 180.0 - lng2 * Math.PI / 180.0;
  var s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2), 2) + Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)));
  s = s * 6378.137;
  s = Math.round(s * 10000) / 10000;
  return s.toFixed(1)
}

// 自定义的存文本toast，需配合模板(组件文件夹下的widget/toast)一起工作
function showToast(config, context) {
  if (!context) context = this
  context.setData({
    toast: {
      status: 1,
      content: config.content
    }
  })
  setTimeout(() => {
    context.setData({
      'toast.status': 2
    })
  }, config.duration || 1500)
}

// 将时间格式18：00 转换成 秒数
var timeStringToTimestamp = function (value = '') {
  const splitedValue = value.toString().split(':')
  return (splitedValue[0] || 0) * 3600 + (splitedValue[1] || 0) * 60
}

// 将非零点timeStamp转换成零点timeStamp 参数：单位为秒
var toZeroTimeStamp = function (timeStamp) {
  const temp = new Date(timeStamp * 1000)
  const year = temp.getFullYear()
  const month = temp.getMonth()
  const date = temp.getDate()
  return new Date(year, month, date).getTime() / 1000
}
const formatFloat = function (f,type) {
  // js浮点数处理
  // f = Math.round(f)
  let falg = false
  if (f > 99999) {
    falg = true
    f = f / 10000
  }
  var m = Math.pow(10, 2)
  // console.log(parseInt(f * m, 10) / m)
  if (falg) {
    return parseInt(f * m, 10) / m + '万'
  } else {
    return parseInt(f * m, 10) / m
  }
}

let getCurrentPageUrl = () => {
  let Pages = getCurrentPages()
  let currentPage = Pages[Pages.length - 1]
  let url = currentPage.__route__
  return url
}

let getCurrentPageUrlWithArgs = () => {
  let Pages = getCurrentPages()
  let currentPage = Pages[Pages.length - 1]
  let url = currentPage.__route__
  let options = currentPage.options

  // 拼接url的參數
  let urlWithArgs = url + '?'
  for (let key in options) {
    let value = options[key]
    urlWithArgs += `${key}=${value}&`
  }

  urlWithArgs = urlWithArgs.substring(0, urlWithArgs.length -1)
  return urlWithArgs
}


module.exports = {
  getCurrentPageUrl,
  getCurrentPageUrlWithArgs,
  add, // 加
  sub, // 减
  mul, // 乘
  div, // 除
  checkPhone, // 核对电话号码
  filterPrice, // 价格过滤器
  format,
  imgProcess,
  formatFloat, // 浮点数处理
  getNow, // 是否是今天
  calcDistance, // 计算地球上两点之间的距离 已经两点的经纬度 单位为度
  showToast, // 自定义的存文本toast，需配合模板(组件文件夹下的widget/toast)一起工作
  timeStringToTimestamp: timeStringToTimestamp, // 将时间格式18：00 转换成 秒数
  toZeroTimeStamp: toZeroTimeStamp // 将非零点timeStamp转换成零点timeStamp
}
