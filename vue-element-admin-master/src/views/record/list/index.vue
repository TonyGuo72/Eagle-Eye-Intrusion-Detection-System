<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.id" placeholder="ID" style="width: 100px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.camera" placeholder="摄像头" clearable style="width: 90px" class="filter-item">
        <el-option v-for="item in cameraTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查找
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="dialog_Visible=true">
        查看回放
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="dialog_Visiblee=true">
        入侵统计
      </el-button>
    </div>

    <el-table
      :key="table_Key"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="摄像头" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.camera }}</span>
        </template>
      </el-table-column>
      <el-table-column label="日期" width="230px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.date }}</span>
        </template>
      </el-table-column>
      <el-table-column label="时间" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="截图" width="110px" align="center">
        <template slot-scope="{row}">
          <el-image style="width: 80px; height: 60px" :src="`${postsrc}${row.imgurl}`" :preview-src-list="[`${postsrc}${row.imgurl}`]">
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </template>
      </el-table-column>
<!--      <el-table-column prop="hotVideoPath" label="视频回放" align="center" show-overflow-tooltip>
        <template slot-scope="{row}">
          <div class="video">
            <el-dialog
              title="播放视频"
              width="72%"
              append-to-body
              top="20px"
              :visible.sync="dialogVisible"
              v-if="dialogVisible"
              @closed="closeDialog"
            >

              <video
                width="100%"
                autoplay="autoplay"
                :src="playvideo"
                :poster="playvideo"
                controls="controls"

                id="video"
                preload
              ></video>
            </el-dialog>
            &lt;!&ndash; 页面table显示的video标签 &ndash;&gt;
            <video
              :src="row.videourl"
              width="100"
              preload
            ></video>
            <i
              class="el-icon-video-play playIcon"
              @click="handleCheck(row)"
            ></i>
          </div>
        </template>
      </el-table-column>-->
      <el-table-column label="操作" align="center" width="110" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button v-permission="['admin']" size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getRecordList" />

    <el-dialog :visible.sync="dialog_Visible" v-if="dialog_Visible" style="width: 110%;margin-left: -50px"  @close="dialog_Visible=false">
      <el-image style="width: 800px;height: 640px;position: center" :src="playvideo" ></el-image>
    </el-dialog>

    <el-dialog :visible.sync="dialog_Visiblee" v-if="dialog_Visiblee" style="width: 100%" center @close="dialog_Visiblee=false">
      <div class="block" v-for="item in chartsrc">
        <span class="demonstration"></span>
        <el-image :src="item.url" fit="contain" :preview-src-list="[item.url]"></el-image>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import { deleteRecordData, fetchRecord, fetchRecordList } from '@/api/record'
import permission from '@/directive/permission/index.js'
import { fetchStaff } from '@/api/staffadmin'


const cameraTypeOptions = [
  { key: '1', display_name: '摄像头1' },
  { key: '2', display_name: '摄像头2' }
]

const cameraTypeKeyValue = cameraTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'recordTable',
  components: { Pagination },
  directives: { waves ,permission},
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    cameraFilter(camera) {
      return cameraTypeKeyValue[camera]
    }
  },
  data() {
    return {
      table_Key: 0,
      list: null,
      total: 0,
      listLoading: true,
      dialog_Visible: false, // 视频播放弹窗
      dialog_Visiblee:false,
      playvideo: 'http://192.168.98.179:5000/video', // 存储用户点击的视频播放链接
      postsrc:'http://192.168.98.179:5000/',
      chartsrc:[{url:'http://192.168.98.179:5000/cameraindex_image',text:'摄像头统计'},{url:'http://192.168.43.169:5000/time_image',text:'时间统计'}],
      listQuery: {
        page: 1,
        limit: 20,
        id: undefined,
        date:undefined,
        camera:undefined,
        start_time:undefined,
        imgurl:undefined,
        videourl:undefined,
        sort: '+id'
      },
      cameraTypeOptions,
      sortOptions: [{ label: 'ID升序', key: '+id' }, { label: 'ID降序', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        page: 1,
        limit: 20,
        id: undefined,
        date:undefined,
        camera:undefined,
        start_time:undefined,
        imgurl:undefined,
        videourl:undefined,
        sort: '+id',
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      downloadLoading: false
    }
  },
  created() {
    this.getRecordList()
  },
  methods: {
    getRecordList() {
      this.listLoading = true
      fetchRecordList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.listLoading = true
      fetchRecord(this.listQuery.id).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        console.log(this.list)
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    sortChange(data) {
      const { prop, order } = data

      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        date:undefined,
        start_time:undefined,
        imgurl:undefined,
        id: undefined,
      }
    },
    handleCheck(row) {
      this.playvideo = row.videourl // 存储用户点击的视频播放链接
      this.dialogVisible = true
    },
    closeDialog(){
      this.dialogVisible=false
    },
    handleDelete(row, index) {
      this.temp = Object.assign({}, row)
      this.$confirm('此操作将永久删除该入侵信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.deleteData()
        this.list.splice(index, 1)
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    deleteData() {
      const tempData = Object.assign({}, this.temp)
      deleteRecordData(tempData).then(() => {
        const index = this.list.findIndex(v => v.id === this.temp.id)
        this.list.splice(index, 1, this.temp)
        this.$notify({
          title: 'Success',
          message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
  }
}
</script>

<style>


</style>
