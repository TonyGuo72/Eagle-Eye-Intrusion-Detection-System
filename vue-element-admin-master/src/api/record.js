import request from '@/utils/request'

export function fetchRecordList(query) {
  return request({
    url: '/record/list',
    method: 'get',
    params:query
  })
}

export function deleteRecordData(data) {
  return request({
    url: '/record/delete',
    method: 'post',
    data
  })
}

export function fetchRecord(id) {
  return request({
    url: '/record/search',
    method: 'get',
    params: { id }
  })
}
