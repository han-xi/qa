<template>
  <div id="svgContainer" >
    <svg width="220" height="220" VIEWBOX="0 0 220 220">
      <circle
        cx="110"
        cy="110"
        r="100"
        stroke-width="8"
        stroke="#D1D3D7"
        fill="none"
      ></circle>
      <circle
        cx="110"
        cy="110"
        r="100"
        stroke-width="8"
        stroke="#00A5E0"
        fill="none"
        transform="matrix(0,-1,1,0,0,220)"
        stroke-dasharray="1069 0"
      ></circle>
    </svg>
    <span id="leftTime" style="font-size:40px">3</span>
  </div>
</template>

<script>
//获得第二个圆的引用
export default {
  name: "StartTime",
  setup(props,context) {
    // context作用是获取上下文对象，
    // 如果setup写法为setup(props, { emit })的方式的话，下面的context可以省略
    const init = () => {
      let circle = document.getElementsByTagName("circle")[1];
      let initTime = 3;
      let lefttime = setInterval(function () {
        initTime--;
        if (initTime < 0) {
          clearInterval(lefttime);
          context.emit("listen", true)
          initTime = 3;
        }
        let leftTimeDom = document.getElementById("leftTime")
        leftTimeDom.innerHTML=initTime;
        let percent = initTime / 3;
        //圆的周长
        let perimeter = Math.PI * 2 * 50;
        //stroke-dasharray属性的两个参数和必须为周长
        circle.setAttribute(
          "stroke-dasharray",
          perimeter * percent + " " + perimeter * (1 - percent)
        );
      }, 1000);
      
    };

    return {
      init
    }
  },
  mounted(){
    this.init()
  },
};
</script>
<style lang="less" scoped>
#svgContainer {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  top:20%;
}
#svgContainer > svg {
  position: absolute;
}
circle {
  -webkit-transition: stroke-dasharray 0.25s;
  transition: stroke-dasharray 0.25s;
}
</style>