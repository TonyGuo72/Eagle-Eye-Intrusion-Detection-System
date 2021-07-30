<template>
  <div id="customPositionDiv">
    <div style="background-color: #c0c0c0;
                    margin:0 auto ; display:-webkit-box;
                    -webkit-box-align:center; -webkit-box-pack:center; ">
      <div @mousedown="mousedown" @mousemove="mousemove"
           @mouseup="mouseup" @Mouseleave="Mouseleave" :style="imgstyle">
        <img :src="imgSrc" :style="imgstyle">
        <canvas id="canvas" ref="table" :width="canvasWidth" :height="canvasHeight" :style="canvasstyle"></canvas>
      </div>
    </div>
    <div style="z-index: inherit;text-align: right ;margin:10px 0 0 0">
            <span slot="footer" class="dialog-footer">
                <el-button @click="customClose()">取 消</el-button>
                <el-button type="primary" @click="customQuery">确 定</el-button>
            </span>
    </div>
  </div>

</template>
<style lang="scss">

</style>
<script>

import vue from 'vue';

export default {
  name: 'canvasDraw',
  props: ['imgSrc'],
  data() {
    return {

      //  customPositionShow:false, //自定义位置
      //   showclose:false,
      url:'',
      startX: '',  //画画开始的X坐标
      startY: '',  //画画开始的Y坐标
      endX: '',    //画画结束的X坐标
      endY: '',    //画画结束的Y坐标
      isMouseDownInCanvas: '', //鼠标是否按下
      customcxt: '',      // cxt
      customRwidth: '',    //原图与展示图片的宽度比
      customRheight: '',   //原图与展示图片的高度比
      imgstyle: '',        //根据图片大小自适应样式
      canvasstyle: '',     //根据图片大小canvas自适应样式 居中显示
      dialogstyle:'',
      canvasWidth: '',     //根据图片大小自适应canvas宽
      canvasHeight: '',    //根据图片大小自适应canvas高
      DivWidth: 710,      //最大宽度
      DivHeight: 740,      //最大高度
      list:[],
    };
  },
  watch: {
    'imgSrc': function () {
      this.show();
    },

  },
  mounted() {
    this.show();
  },

  methods: {
    //取消时返回组件调用处所需的数据
    customClose() {
      this.list=[];
      this.customcxt.clearRect(0, 0, this.DivWidth, this.DivHeight);
      this.$emit('hideDialog');
      //this.$emit('custom', { 'type': 1, 'data': '' });

    },
    //确定时返回组件调用处所需的数据
    customQuery() {
      this.customcxt.clearRect(0, 0, this.DivWidth, this.DivHeight);
      //根据绘制进行图片裁剪
      let newlist = [];
      for(let i=0;i<this.list.length;i++){
        let point=[];
        point=[this.list[i].start_x,this.list[i].start_y];
        newlist[i*2]=point;
        let point1=[];
        point1=[this.list[i].end_x,this.list[i].end_y];
        newlist[i*2+1]=point1;
      }

      this.$emit('getpointlist', newlist);
      this.list=[];
      this.$emit('hideDialog');
    },
    beforeDestroy(){
      this.destroy()
    },
    // dialog展示自定义矩形框画板，
    // 计算img与canvas标签自适应图片的大小
    show() {
      vue.nextTick(_ => {
        let customCanvas = this.$refs.table;// canvas显示层
        this.customcxt = customCanvas.getContext("2d");
        let img = new Image();
        img.src = this.imgSrc;
        let that = this;
        img.onload = function () {

          let canvasleft = 0;
          let canvastop = 0;
          /*let WrH = img.width / img.height;             //图片宽高比
          let RWrH = that.DivWidth / that.DivHeight;    //放置图片DIV的宽高比
          let aa = 0;
          // 根据宽高比大小判断确定自适应的宽和高
          if (RWrH > WrH) {
            aa = that.DivHeight / img.height;
            that.canvasHeight = that.DivHeight;
            that.canvasWidth = img.width * aa;
            canvasleft = (that.DivWidth - that.canvasWidth) / 2
          } else {
            aa = that.DivWidth / img.width;
            that.canvasHeight = img.height * aa;
            that.canvasWidth = that.DivWidth;
            canvastop = (that.DivHeight - that.canvasHeight) / 2
          }*/
          that.canvasWidth=img.width;
          that.canvasHeight=img.height;
          that.imgstyle = ' position: relative;  width:' + that.canvasWidth
            + ' px; height:' + that.canvasHeight + 'px'; //img浮动定位居中显示
          /*that.customRwidth = that.canvasWidth / img.width; //原图与展示图片的宽高比
          that.customRheight = that.canvasHeight / img.height;*/

          that.canvasstyle = 'position: absolute;left: 0'/* + canvasleft*/
            + 'px; top: 0'/* + canvastop*/ + 'px;' //canvas浮动定位


        };
      })

    },
    //鼠标按下时执行
    mousedown(e) {
      this.isMouseDownInCanvas = true;
      // 鼠标按下时开始位置与结束位置相同
      // 防止鼠标在画完矩形后 点击图画形成第二个图形
      this.endX = e.offsetX;
      this.endY = e.offsetY;
      this.startX = e.offsetX;
      this.startY = e.offsetY;
      this.mousemove(e)
    },

    //鼠标移动式时执行
    mousemove(e) {
      this.drawLine(e);
    },
    drawLine(e){
      if (this.isMouseDownInCanvas) { // 当鼠标有按下操作时执行
        this.endX = e.offsetX;
        this.endY = e.offsetY;

        // 清除指定区域的所有像素
        this.customcxt.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
        this.customcxt.strokeStyle = " #00ff00"; //颜色
        this.customcxt.lineWidth = "2";  //宽度
        this.list.forEach((value) => {
          this.customcxt.moveTo(value.start_x,value.start_y);
          this.customcxt.lineTo(value.end_x,value.end_y);
          this.customcxt.stroke();
        })

        this.customcxt.beginPath();
        this.customcxt.strokeStyle = " #00ff00";
        this.customcxt.lineWidth = "2";
        this.customcxt.moveTo(this.startX,this.startY);
        this.customcxt.lineTo(e.offsetX,e.offsetY);
        this.customcxt.stroke();
      }
    },
    //鼠标松开时执行
    mouseup(e) {
      this.isMouseDownInCanvas = false;
      this.list.push({
        start_x:this.startX,
        start_y:this.startY,
        end_x:this.endX,
        end_y:this.endY,
      })
    },

    Mouseleave(e) {
      this.isMouseDownInCanvas = false
    },
  },
}
</script>
