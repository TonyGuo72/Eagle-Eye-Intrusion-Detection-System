import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/vue-admin-template/table/list',
    method: 'get',
    params
  })
}

export function fetchTableData(query) {
  return request({
    url: '/api/test/',
    method: 'GET',
    params: query
  })
}
