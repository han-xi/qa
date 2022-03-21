<template>
  <div style="height: 100%">
    <div :style="{ height: '64px', padding: '24px 0' }">
      <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes, paths }">
          <span v-if="routes.indexOf(route) === routes.length - 1">
            {{ route.breadcrumbName }}
          </span>
          <router-link
            v-else-if="routes.indexOf(route) === 0"
            :to="`${basePath}/${paths.join('/')}`"
          >
            <home-outlined /> {{ route.breadcrumbName }}
          </router-link>
          <router-link
            v-else-if="route.breadcrumbName === 'class'"
            :to="`${basePath}/${paths[1]}/${paths[2]}/${params_cid}/${params_cname}`"
          >
            {{ route.breadcrumbName }}
          </router-link>

          <router-link v-else :to="`${basePath}/${paths[1]}`">
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
      <a-list
        class="demo-loadmore-list"
        :loading="loading"
        item-layout="horizontal"
        :data-source="dataList"
        ><template #header>
          <a-typography-title>错题库</a-typography-title>
        </template>
        <template #loadMore>
          <div
            :style="{
              textAlign: 'center',
              marginTop: '12px',
              height: '32px',
              lineHeight: '32px',
            }"
          >
            <a-spin v-if="loadingMore" />
            <a-button v-else @click="loadMore" :disabled="!isremain"
              >loading more</a-button
            >
          </div>
        </template>
        <template #renderItem="{ item }">
          <a-list-item>
      
            <a-list-item-meta :description="item.updatetime">
              <template #title>
                <router-link
                  style="color: #1890ff !important"
                  :to="`/classlist/class/${params_cid}/${params_cname}/studentwrongquestion/${params_sid}/question/${item.problem_id}`"
                  >{{ item.id }}.{{ item.title }}</router-link
                >
              </template>
              <template #avatar>
                <!-- <a-avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" /> -->
              </template>
            </a-list-item-meta>
            <div>{{ item.num }}</div>
          </a-list-item>
        </template>
      </a-list>
    </div>
  </div>
</template>
<script>
import { ref, defineComponent, onMounted } from "vue";
import { HomeOutlined } from "@ant-design/icons-vue";
import question from "../apis/question";
import { useRoute } from "vue-router";
import { message } from "ant-design-vue";
export default defineComponent({
  name: "StudentQuestionList",
  components: {
    HomeOutlined,
  },

  setup() {
    const route = useRoute();
    const params_cid = ref("");
    const params_cname = ref("");
    const params_sid =ref("")
    params_cid.value = route.params.cid;
    params_cname.value = route.params.cname;
    params_sid.value =route.params.sid
    const routes = ref([
      {
        path: "main",
        breadcrumbName: "home",
      },
      {
        path: "classlist",
        breadcrumbName: "classlist",
      },
      {
        path: "class",
        breadcrumbName: "class",
      },
        {
        path: "studentwrongquestion",
        breadcrumbName: "studentwrongquestion",
      },
    ]);
    onMounted(() => {
      loadMore();
    });
    let loading = ref(true);
    let loadingMore = ref(false);

    let isremain = ref(true);
    // const count = ref(1);
    let page = ref(1);
    const dataList = ref([]);
    let delflag = ref(false);
    const loadMore = () => {
      loading.value = false;
      loadingMore.value = true;
      //loading.value = !loading.value
      if (delflag.value) {
        let postdata = {
          page: 1,
          size: page.value * 5,
          user_id :route.params.sid,
          class_id:route.params.cid
        };
        question
          .getwronglist(postdata)
          .then((res) => {
            dataList.value = [];
            dataList.value.push(...res.data["result"]);
            dataList.value.forEach((element, index) => {
              element["id"] = index + 1;
            });
            ++page.value;
            delflag.value = !delflag.value;
            isremain.value = res.data["isremain"];
            loadingMore.value = false;
          })
          .catch((err) => {
            console.log(err);
            loadingMore.value = false;
          });
      } else {
        let postdata = {
          page: page.value,
           user_id :route.params.sid,
             class_id:route.params.cid
        };
        question
          .getwronglist(postdata)
          .then((res) => {
            dataList.value.push(...res.data["result"]);
            dataList.value.forEach((element, index) => {
              element["id"] = index + 1;
            });
            ++page.value;

            isremain.value = res.data["isremain"];
            loadingMore.value = false;
          })
          .catch((err) => {
            console.log(err);
            loadingMore.value = false;
          });
      }

      // loadingMore.value = true
    };
    const deleteQuestion = (val) => {
      const val_index = dataList.value.indexOf(val);
      dataList.value.splice(val_index, 1);
      dataList.value.forEach((element) => {
        if (element.id > val_index) {
          --element.id;
        }
      });
      let postdata = {
        problem_id: val.problem_id,
      };
      question
        .deletewrong(postdata)
        .then((res) => {
          delflag.value = true;
          message.success(res.data["message"]);
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return {
      routes,
      basePath: "",
      deleteQuestion,
      loading,
      loadingMore,
      dataList,
      loadMore,
      isremain,
      params_cid,
      params_cname,
      params_sid
    };
  },
});
</script>
<style scoped>
.demo-loadmore-list {
  min-height: 350px;
}
</style>