<template>
  <div class="app-container">
<!--    <div class="filter-container">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item>
          <el-select v-model="camera" placeholder="请选择摄像头" clearable style="width: 150px" class="filter-item" @change="handleFilter">
            <el-option v-for="item in cameraOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="dialogVisable=true">划定入侵范围</el-button>
        </el-form-item>
      </el-form>
    </div>-->
    <div class="components-container">
    <div v-for="item in video_src"
         class="camera" >
      <el-image
        style="width: 600px; height: 450px;"
        :src="item.url"
        fit="contain"
        :preview-src-list="[item.url]"></el-image>
        <el-button @click="dialogVisable=true;temp_src=item.url;camera=item.index">划定范围</el-button>
    </div>
    </div>

    <el-dialog :visible.sync="dialogVisable" style="width: 100%">
      <draw :img-src="temp_src"  @hideDialog="hideDialog" @getpointlist="getpointlist"></draw>
    </el-dialog>
  </div>
</template>

<script>
import { drawArea, fetchAlert, fetchCamera} from '@/api/camara'
import Draw from './components/draw'
import imgtest from '/src/views/watch/test1.jpg'
import imgtest1 from '/src/views/watch/test2.jpg'

  export default {
    filters: {
    },
    components:{Draw},
    data() {
      return {
        timer:null,
        video_src:[],
        dialogVisable:false,
        tableKey: 0,
        list: null,
        listLoading: true,
        camera: 1,
        videosrc:'http://172.20.10.5:5000/video_start',
        temp_src:'',
/*        camaraTypeOptions,*/
        cameraOptions:[{key:'1',display_name:'摄像头1'},{key:'2',display_name: '摄像头2'}],
        pointlist:[]
      }
    },
    created() {
      this.camera=this.cameraOptions[0].key
      this.getCamera()
    },
    mounted() {
      let that=this
      let time=3000
      this.timer=setInterval(function(){
        setTimeout(()=>{
          //this.getAlert()
          fetchAlert().then(response=>{
            const{value,data}=response
            if(value===20000){
              that.$notify({
                title: 'warring',
                message: '检测到入侵',
                type: 'error',
                duration: 2000
              })
            }
          })
        },0)
      },time)
    },
    beforeDestroy() {
      clearInterval(this.timer)
    },
    methods: {
      getCamera() {
        this.listLoading = true
        for(let i=1;i<=this.camera;i++){
          this.video_src[i-1]= {index:i,url:`${this.videosrc}${i}`}
        }
        /*this.video_src[0]=imgtest
        this.video_src[1]=imgtest1*/
      },
      handleFilter() {
        //this.getCamera()
      },
      hideDialog(){
        this.dialogVisable=false;
      },
      getpointlist:function(arr){
        this.listLoading = true
        console.log(arr)
        this.pointlist=arr
        drawArea({point:this.pointlist,camera:this.camera}).then(()=>{
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
      },
      getAlert(){
        fetchAlert().then(response=>{
          const{value,data}=response
          if(value===20000){
            this.$message({
              message:'warning',
              type:'warning',
            });
          }
        })
      },
      changeCamera(){

      }
    }
  }
</script>
<style>
.camera{
  padding: 30px 0;
  text-align: center;
  border-right: 1px solid #dfe4ea;
  display: inline-block;
  width: 600px;
  box-sizing: border-box;
  vertical-align: top;
}
</style>
