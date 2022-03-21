<template>
  <div>
    <a-card style="width: 100%; height: 400px">
      <template #title>
        <a-tooltip>
    <template #title>
      {{props.Index}}.{{props.Title}}
    </template>
        <a-typography-title  :ellipsis='true' :level="3"
        :content="`${props.Index}.${props.Title}`"
          ></a-typography-title
        >
        
        </a-tooltip></template
      >
      <template #extra
        ><a href="#"
          ><a-button
            v-if="auth.user.authenticated&&!props.IsCollected &&!collectflag"
            type="primary"
            class="btn"
            @click="clickcollcet"
            >+收藏</a-button
            
          >
          <a-button
            v-if="auth.user.authenticated&&(props.IsCollected||collectflag)"
            type="primary"
            class="btn"
            disabled
            @click="clickcollcet"
            >已收藏</a-button>
          </a
        ></template
      >
      <a-radio-group v-model:value="SelectNum">
        <a-radio
         :style="radioStyle" 
          v-for="(item, i) in props.Options"
          :value="i + 1"
          :key="i"
          :disabled="disabled"
          ><a-typography-title
            :level="3"
            type="success"
            v-if="SelectNum !== '' && i + 1 === props.Answer"
            >{{ OP[i + 1] }}.{{ item }}</a-typography-title
          ><a-typography-title
            type="danger"
            :level="5"
            v-else-if="SelectNum == i + 1 && i + 1 != props.Answer"
            >{{ OP[i + 1] }}.{{ item }}</a-typography-title
          ><a-typography-title :level="5" v-else
            >{{ OP[i + 1] }}.{{ item }}</a-typography-title
          ></a-radio
        >
      </a-radio-group>
    </a-card>
    <br />
    <a-card
      v-if="SelectNum !== '' && SelectNum !== props.Answer"
      size="small"
      style="width: 100%; height: 100px"
    >
      <a-typography-title :level="3" 
        >正确答案 :{{ OP[props.Answer] }}</a-typography-title
      >
    </a-card>
  </div>
  <div
    v-if="end"
    style="position: absolute; top: 50%; left: 50%; width: 200px; z-index: 10"
  >
    <a-button
      danger
      shape="round"
      style="right: 20px; width: 50%"
      @click="Pre"
      class="btn"
    >
      <template #icon> <ArrowLeftOutlined /></template>
    </a-button>
    <a-button
      danger
      shape="round"
      style="left: 20px; width: 50%"
      @click="Next"
      class="btn"
      ><template #icon> <ArrowRightOutlined /></template
    ></a-button>
  </div>
</template>
<script>
import { ref, reactive, watch } from "vue";
import { ArrowLeftOutlined, ArrowRightOutlined } from "@ant-design/icons-vue";
import question from "../apis/question";
import auth from "../auth";
import { message } from "ant-design-vue";
import { useRouter } from "vue-router";
//import { query_list } from "../apis/query";
export default {
  name: "QuestionShow",
  components: {
    ArrowLeftOutlined,
    ArrowRightOutlined,
  },
  props: {
    Problem_id: String,
    Index: Number,
    Title: String,
    Options: Array,
    Answer: Number,
    IsCollected:{
      type:Boolean,
      default:false
    }
  },
  setup(props, context) {
    const OP = reactive({
      1: "A",
      2: "B",
      3: "C",
      4: "D",
    });
    let collectflag = ref(false)
    let SelectNum = ref("");
    let end = ref(false);
    let disabled = ref(false);
    const radioStyle = reactive({
      display: "block",
      // height: "80px",
      lineHeight: "20px",
    });
    watch(props,()=>{
      collectflag.value=false
    })

    watch(SelectNum, () => {
      if (SelectNum.value !== "") {
        disabled.value = true;
        end.value = true;
        if (auth.user.authenticated && props.Answer !== SelectNum.value) {
          let postdata = {
            problem_id: props.Problem_id,
            wrong_answer: SelectNum.value,
          };
          question
            .addwrong(postdata)
            .then((res) => {
              console.log(res);
            })
            .catch((error) => {
              console.log(error);
            });
        }
      }
    });
    watch(
      () => props.Index,
      () => {
        SelectNum.value = "";
        disabled.value = false;
        end.value = false;
      },
      {
        deep: true,
        immediate: true,
      }
    );
    let router = useRouter();
    let clickcollcet = () => {
      if (auth.user.authenticated) {
        let postdata = {
          problem_id: props.Problem_id,
        };
        question
          .addcollect(postdata)
          .then((res) => {
collectflag.value = true
            message.success(res.data["message"]);
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        router.replace("/replace");
      }
    };
    let Next = () => {
      context.emit("listen", "next");
    };
    let Pre = () => {
      context.emit("listen", "pre");
    };
    return {
      radioStyle,
      props,
      SelectNum,
      OP,
      disabled,
      end,
      clickcollcet,
      auth,
      Next,
      Pre,
      collectflag,
    };
  },
};
</script>
<style scoped>
.btn {
  animation: scaleDrew 2.5s ease-in-out infinite;
}

@keyframes scaleDrew {
  /* 定义关键帧、scaleDrew是需要绑定到选择器的关键帧名称 */
  0% {
    transform: scale(1);
  }

  25% {
    transform: scale(1.1);
  }

  50% {
    transform: scale(1);
  }

  75% {
    transform: scale(1.1);
  }
}
</style>
