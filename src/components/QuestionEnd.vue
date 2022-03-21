<template>
      <!-- <a-progress type="circle" :percent="75" /> -->
    
  <a-result v-if='end' title="你真棒，一道错题都没有，继续做题吧">
        <template #icon>
      <smile-twoTone />
    </template>
    <template #extra>
      <a-button key="console" type="primary" @click="goHome">Go Home</a-button>
    </template>
  </a-result>

   <a-result v-else title="Great, we have done all the questions!">
    <template #icon>
      <smile-twoTone />
    </template>
    <template #extra>
      <a-button type="primary" @click="analyse">查看分析</a-button>
    </template>
  </a-result>
</template>
<script>
import { SmileTwoTone } from "@ant-design/icons-vue"
import {useRouter} from "vue-router"
export default {
    name:'QuestionEnd',
    props:{
      end:{
        type:Boolean,
        default:false,
      }
    },
    components:{
        SmileTwoTone
    },
    setup(props,context) {
      const router = useRouter()
        let analyse = ()=>{
            context.emit('listen',true)
        }
        let goHome = ()=>{
          router.replace('/refresh')
        }
        return {
            analyse,props,goHome
           
        }
    },
}
</script>