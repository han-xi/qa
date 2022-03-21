<template>
  <div class="wrap">
    <button class="button rubberBand"  @click="sayToFather1">开始答题</button>
    <button class="button jello" type="dashed" style=" background-color:#18aeff"  @click="sayToFather2">错题库答题</button>
  </div>
</template>
<script>
import { defineComponent } from "vue"
import auth from "../auth"
import { message } from 'ant-design-vue';
export default defineComponent({
  name: "StartButton",
  setup(props, context) {
    // context作用是获取上下文对象，
    // 如果setup写法为setup(props, { emit })的方式的话，下面的context可以省略
    const sayToFather1 = () => {
      context.emit("listen", '1')
    };
    const sayToFather2 = () => {
      if (auth.user.authenticated){
      context.emit("listen", '2')
      }else{
 message.error('请登录');
      }
    };
    return {
      sayToFather1,
      sayToFather2,
    }
  }

  
})
</script>
<style lang="less" scoped>
.wrap {
  //padding: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
:root {
  --primary-color: royalblue;
}
.button {
  font-family: YouYuan ;
  color: #000000d9;
  border: 1px solid #d9d9d9;
  background-color: #b5ff18;
  border-radius: 2px;
  font-size: 40px;
  height: 400px;
  width: 400px;
  margin:10px;
  line-height: 1.4;
  box-shadow: 0 2px #00000004;
  cursor: pointer;
  transform: scale(1);
  animation: jump 0s;
  transition: 0.3s;

  padding-right: 0;
  padding-left: 0;
  text-align: center;
  border-radius: 50%;
}
.button:focus-visible {
  outline: 0;
}

.button[type="dashed"] {
  border-style: dashed;
}
.button[type="text"] {
  border-color: transparent;
  box-shadow: none;
}
.button:not([type]):hover,
.button[type="dashed"]:hover,
.button[type="dashed"]:focus {
  color: var(--primary-color);
  border-color: currentColor;
}
.button[type="text"]:hover {
  background: rgba(0, 0, 0, 0.018);
}
.tada {
  animation: tada 0s;
}
.rubberBand {
  animation: rubberBand 0s;
   animation-duration: 1s;
}
.jello {
  animation: jello 0s;
   animation-duration: 1s;
}
.button:hover {
  //animation-duration: 1s;
  filter: brightness(0.9);
  animation: none;
}

.button.button:active {
  filter: brightness(0.9);
  animation: none;
}
@keyframes tada {
  from {
    transform: scale3d(1, 1, 1);
  }

  10%,
  20% {
    transform: scale3d(0.9, 0.9, 0.9) rotate3d(0, 0, 1, -3deg);
  }

  30%,
  50%,
  70%,
  90% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, 3deg);
  }

  40%,
  60%,
  80% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, -3deg);
  }

  to {
    transform: scale3d(1, 1, 1);
  }
}

@keyframes rubberBand {
  0% {
    -webkit-transform: scaleX(1);
    transform: scaleX(1);
  }

  30% {
    -webkit-transform: scale3d(1.25, 0.75, 1);
    transform: scale3d(1.25, 0.75, 1);
  }

  40% {
    -webkit-transform: scale3d(0.75, 1.25, 1);
    transform: scale3d(0.75, 1.25, 1);
  }

  50% {
    -webkit-transform: scale3d(1.15, 0.85, 1);
    transform: scale3d(1.15, 0.85, 1);
  }

  65% {
    -webkit-transform: scale3d(0.95, 1.05, 1);
    transform: scale3d(0.95, 1.05, 1);
  }

  75% {
    -webkit-transform: scale3d(1.05, 0.95, 1);
    transform: scale3d(1.05, 0.95, 1);
  }

  to {
    -webkit-transform: scaleX(1);
    transform: scaleX(1);
  }
}
@keyframes jello {
  0%,
  11.1%,
  to {
    -webkit-transform: translateZ(0);
    transform: translateZ(0);
  }

  22.2% {
    -webkit-transform: skewX(-12.5deg) skewY(-12.5deg);
    transform: skewX(-12.5deg) skewY(-12.5deg);
  }

  33.3% {
    -webkit-transform: skewX(6.25deg) skewY(6.25deg);
    transform: skewX(6.25deg) skewY(6.25deg);
  }

  44.4% {
    -webkit-transform: skewX(-3.125deg) skewY(-3.125deg);
    transform: skewX(-3.125deg) skewY(-3.125deg);
  }

  55.5% {
    -webkit-transform: skewX(1.5625deg) skewY(1.5625deg);
    transform: skewX(1.5625deg) skewY(1.5625deg);
  }

  66.6% {
    -webkit-transform: skewX(-0.78125deg) skewY(-0.78125deg);
    transform: skewX(-0.78125deg) skewY(-0.78125deg);
  }

  77.7% {
    -webkit-transform: skewX(0.390625deg) skewY(0.390625deg);
    transform: skewX(0.390625deg) skewY(0.390625deg);
  }

  88.8% {
    -webkit-transform: skewX(-0.1953125deg) skewY(-0.1953125deg);
    transform: skewX(-0.1953125deg) skewY(-0.1953125deg);
  }
}
</style>