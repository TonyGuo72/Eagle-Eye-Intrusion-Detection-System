import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/login',
    method: 'get',
    params:token
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

export function signup(data){
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

export function sendEmail(data){
  return request({
    url: '/sendemail',
    method: 'post',
    data
  })
}
