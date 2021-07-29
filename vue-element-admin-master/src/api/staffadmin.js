import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/staff/list',
    method: 'get',
    params: query
  })
}

export function fetchStaff(id) {
  return request({
    url: '/staff/search',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/vue-element-admin/article/pv',
    method: 'get',
    params: { pv }
  })
}

export function createArticle(data) {
  return request({
    url: '/staff/add',
    method: 'post',
    data
  })
}

export function updateArticle(data) {
  return request({
    url: '/staff/edit',
    method: 'post',
    data
  })
}

export function deleteData(data) {
  return request({
    url: '/staff/delete',
    method: 'post',
    data
  })
}
