<template>
  <div style="height: 100%">
    <div :style="{ height: '64px', padding: '24px 0' }">
      <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes, paths }">
          <span v-if="routes.indexOf(route) === routes.length - 1">
            <home-outlined /> {{ route.breadcrumbName }}
          </span>
          <router-link v-else :to="`${basePath}/${paths.join('/')}`">
            {{ route.breadcrumbName }}
          </router-link>
        </template>
      </a-breadcrumb>
    </div>
    <div
      :style="{
        padding: '24px',
        background: '#fff',
        height: 'calc(100% - 64px)',
      }"
    >
      <StartButton
        @listen="listenToBUtton"
        v-if="startbutton_msg_show"
      ></StartButton>
      <start-time v-if="starttime_msg_show" @listen="listenToTime"></start-time>
      <question-show
        v-if="question_msg_show"
        @listen="listenToQuestion"
        :Index="qIndex"
        :Answer="qAnswer"
        :Options="qOptions"
        :Title="qTitle"
        :IsCollected="qIsCollected"
        :Problem_id="qProblem_id"
      ></question-show>
      <question-end
        v-if="end_msg_show"
        :end="isEmpty"
        @listen="listenToEnd"
      ></question-end>
    </div>
  </div>
</template>
<script>
import { HomeOutlined } from "@ant-design/icons-vue";
import StartButton from "../components/StartButton";
import StartTime from "../components/StartTime.vue";
import QuestionShow from "../components/QuestionShow.vue";
import QuestionEnd from "../components/QuestionEnd.vue";
import { ref, watch, onBeforeMount } from "vue";
import question from "../apis/question";
// import QuestionPage from '@/components/QuestionPage.vue';
export default {
  name: "InMain",
  components: {
    StartButton,
    StartTime,
    QuestionShow,
    HomeOutlined,
    QuestionEnd,
  },
  setup() {
    const routes = ref([
      {
        path: "main",
        breadcrumbName: "home",
      },
    ]);
    let startbutton_msg = ref("");
    let startbutton_msg_show = ref(true);
    let starttime_msg_show = ref(false);
    let question_msg_show = ref(false);
    let end_msg_show = ref(false);
    let isEmpty = ref(false);
    let qdata = ref([]);
    let qIndex = ref(0);
    let qProblem_id = ref("");
    let qTitle = ref("");
    let qOptions = ref([]);
    let qAnswer = ref(0);
    let qIsCollected = ref(false);

    let selectButton = ref(0);
    let page = ref(1);
    onBeforeMount(async () => {});
    watch(qdata.value, (newdata) => {
      if (newdata.length === 5) {
        ++page.value;
        getquestionlist();
      }
    });
    let getquestionlist = async () => {
      let postdata = {
        page: page.value,
      };
      if (selectButton.value === 1) {
        await question.getquestionlist(postdata).then((res) => {
          // qdata.value.unshift(...res.data["result"]);
          res.data["result"].forEach((element) => {
            qdata.value.unshift(element);
          });
        });
      } else if (selectButton.value === 2) {
        await question.getwronglistforhome(postdata).then((res) => {
          res.data["result"].forEach((element) => {
            qdata.value.unshift(element);
          });
        });
      }
    };

    let listenToBUtton = async (val) => {
      startbutton_msg.value = val; // 使用ref包裹的数据，需要通过.value的形式访问他的值
      if (val !== "") {
        startbutton_msg_show.value = false;

        if (val === "1") {
          selectButton.value = 1;
          await getquestionlist();
        } else if (val === "2") {
          selectButton.value = 2;
          await getquestionlist();
        }
        if (qdata.value.length>0) {
          console.log('qdata',qdata.value)
          starttime_msg_show.value = true;
          let temp = qdata.value.pop();
          qIndex.value = Number(temp["Index"]);
          qOptions.value = eval(temp["Options"]);
          qAnswer.value = Number(temp["Answer"]);
          qProblem_id.value = temp["Problem_id"];
          qIsCollected.value = temp["IsCollected"];
          qTitle.value = temp["Title"];
        } else {
          starttime_msg_show.value = false;
          isEmpty.value = true;
          end_msg_show.value =true
        }
      }
    };
    let listenToTime = (val) => {
      starttime_msg_show.value = !val;
      question_msg_show.value = true;
    };
    let listenToQuestion = (val) => {
      if (val === "next") {
        // console.log(qdata.value.length);
        if (qdata.value.length > 0) {
          let temp = qdata.value.pop();
          qIndex.value = Number(temp["Index"]);
          qOptions.value = eval(temp["Options"]);
          qAnswer.value = Number(temp["Answer"]);
          qProblem_id.value = temp["Problem_id"];
          qIsCollected.value = temp["IsCollected"];
          qTitle.value = temp["Title"];
        } else {
          question_msg_show.value = false;
          end_msg_show.value = true;
        }
      } else {
        console.log();
      }
    };
    let listenToEnd = (val) => {
      if (val) {
        end_msg_show.value = false;
      }
    };
    return {
      startbutton_msg,
      startbutton_msg_show,
      starttime_msg_show,
      question_msg_show,
      listenToBUtton,
      listenToTime,
      listenToQuestion,
      listenToEnd,
      routes,
      basePath: "",
      getquestionlist,
      qIndex,
      qProblem_id,
      qTitle,
      qOptions,
      qAnswer,
      qIsCollected,
      end_msg_show,
      isEmpty
    };
  },
};
</script>


<style scoped>
</style>
