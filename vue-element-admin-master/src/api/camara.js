import request from '@/utils/request'

export function fetchCamera(query) {
  return request({
    url: '/camera',
    method: 'get',
    params: query
  })
}

export function fetchAlert() {
  return request({
    url: '/alert',
    method: 'get'
  })
}

export function drawArea(data) {
  return request({
    url: '/drawarea',
    method: 'post',
    data
  })
}
