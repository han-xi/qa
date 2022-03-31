<template>
  <a-table
    :data-source="data"
    :columns="columns"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
  >
    <template
      #filterDropdown="{
        setSelectedKeys,
        selectedKeys,
        confirm,
        clearFilters,
        column,
      }"
    >
      <div style="padding: 8px">
        <a-input
          ref="searchInput"
          :placeholder="`Search ${column.dataIndex}`"
          :value="selectedKeys[0]"
          style="width: 188px; margin-bottom: 8px; display: block"
          @change="
            (e) => setSelectedKeys(e.target.value ? [e.target.value] : [])
          "
          @pressEnter="handleSearch(selectedKeys, confirm, column.dataIndex)"
        />
        <a-button
          type="primary"
          size="small"
          style="width: 90px; margin-right: 8px"
          @click="handleSearch(selectedKeys, confirm, column.dataIndex)"
        >
          <template #icon><SearchOutlined /></template>
          Search
        </a-button>
        <a-button
          size="small"
          style="width: 90px"
          @click="handleReset(clearFilters)"
        >
          Reset
        </a-button>
      </div>
    </template>

    <template #filterIcon="filtered">
      <search-outlined :style="{ color: filtered ? '#108ee9' : undefined }" />
    </template>
    <template #customRender="{ text, column, record }">
      <span v-if="searchText && searchedColumn === column.dataIndex">
        <template
          v-for="(fragment, i) in text
            .toString()
            .split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
        >
          <mark
            v-if="fragment.toLowerCase() === searchText.toLowerCase()"
            class="highlight"
            :key="i"
          >
            <a @click="enterUserInfo(record)" :key="i">{{ fragment }}</a>
          </mark>
          <template v-else>
            <a @click="enterUserInfo(record)" :key="i">{{
              fragment
            }}</a></template
          >
        </template>
      </span>
      <template v-else>
        <a @click="enterUserInfo(record)"> {{ text }}</a>
      </template>
    </template>
  
    <template #customRender1="{ text,column}">
     <span v-if="searchText && searchedColumn === column.dataIndex">
        <template
          v-for="(fragment, i) in text
            .toString()
            .split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
        >
          <mark
            v-if="fragment.toLowerCase() === searchText.toLowerCase()"
            class="highlight"
            :key="i"
          >
            {{ fragment }}
          </mark>
          <template v-else> {{ fragment }}</template>
        </template>
      </span> 
      <template v-else>
        {{ text }}
      </template>
    </template>
    <template #admit="{ record }">
      <a-button
        type="primary"
        @click="admit(record.username, record)"
        :disabled="record.isoperated"
        >准许</a-button
      >
    </template>
    <template #notadmit="{ record }">
      <a-button
        type="primary"
        @click="notadmit(record.username, record)"
        :disabled="record.isoperated"
        >驳回</a-button
      >
    </template>
  </a-table>
  <student-info
    :ismodel="ismodel_user"
    :visible="modelvisible1"
    :isstudent="isstudent"
    :user_id="record_username"
    @listen="listenuser"
  ></student-info>
</template>
<script>
import { SearchOutlined } from "@ant-design/icons-vue";
import {
  onBeforeMount,
  defineComponent,
  reactive,
  ref,
  toRefs,
  computed,
} from "vue";
// import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import user from "../apis/user";
import auth from "../auth";
import StudentInfo from "../components/StudentInfo.vue";
export default defineComponent({
  components: {
    SearchOutlined,
    StudentInfo,
  },
  name: "TableApplyUpgrade",
  setup() {
    const OP = {
      2:'教师',
      3:'管理员'
    }
    let loading = ref(true);
    let total = ref(0);
    const data = ref([]);
    let current = ref(1);
    let sorterOrder = ref("");
    onBeforeMount(() => {
      getupgradepermissionlist();
    });
    const getupgradepermissionlist = () => {
      const postdata = {
        current: current.value,
        sorter: sorterOrder.value,
        search: state.searchText,
        search1: state.searchText1,
      };

      user
        .getupgradepermissionlist(postdata)
        .then((res) => {
          data.value = res.data["result"];
          total.value = res.data["total"];

          // total.value = data.value.length;
          loading.value = false;
        })
        .catch((error) => {
          console.log(error);
          loading.value = false;

          message.error(error["message"]);
        });
    };
    const state = reactive({
      searchText: "",
      searchText1: "",
      searchedColumn: "",
      searchedColumn1: "",
    });
    const searchInput = ref();
    // const convertDateFromString = (dateString) => {
    //   if (dateString) {
    //     var arr1 = dateString.split(" ");
    //     var sdate = arr1[0].split("-");
    //     var date = new Date(sdate[0], sdate[1] - 1, sdate[2]);
    //     return date;
    //   }
    // };
    const columns = [
      {
        title: "申请人",
        dataIndex: "username",
        key: "name",
        slots: {
          filterDropdown: "filterDropdown",
          filterIcon: "filterIcon",
          customRender: "customRender",
        },
        onFilter: (value, record) =>
          record.username
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
          if (visible) {
            setTimeout(() => {
              // console.log(searchInput.value);
              searchInput.value.focus();
            }, 100);
          }
        },
      },
      {
        title: "申请权限",
        dataIndex: "usertype",
        key: "usertype",
        slots: {
          filterDropdown: "filterDropdown",
          filterIcon: "filterIcon",
          customRender: "customRender1",
        },
        onFilter: (value, record) =>
          record.usertype
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
          if (visible) {
            setTimeout(() => {
              // console.log(searchInput.value);
              searchInput.value.focus();
            }, 100);
          }
        },
      },
      {
        title: "申请时间",
        dataIndex: "updatetime",
        key: "updatetime",
        sorter: true,
        // (a, b) => convertDateFromString(a.updatetime) - convertDateFromString(b.updatetime),
        sortDirections: ["descend", "ascend"],
      },
      {
        title: "申请批准",
        slots: { customRender: "admit" },
      },
      {
        title: "驳回申请",
        slots: { customRender: "notadmit" },
      },
    ];
    const pagination = computed(() => ({
      total: total.value,
      current: current.value,
      pageSize: 5,
    }));

    const handleTableChange = (pag, filters, sorter) => {
      (current.value = pag.current), (sorterOrder.value = sorter.order);
      getupgradepermissionlist();
      console.log(sorterOrder.value);
    };
    const handleSearch = (selectedKeys, confirm, dataIndex) => {
      confirm();
      current.value = 1;
      if (dataIndex == "usertype") {
        state.searchText1 = selectedKeys[0];
        state.searchedColumn1 = dataIndex;
      } else {
        state.searchText = selectedKeys[0];
        state.searchedColumn = dataIndex;
      }
      getupgradepermissionlist();
    };

    const handleReset = (clearFilters, dataIndex) => {
      clearFilters();
      if (dataIndex == "usertype") {
        state.searchText1 = "";
        state.searchedColumn1 = "";
      } else {
        state.searchText = "";
        state.searchedColumn = "";
      }

      getupgradepermissionlist();
    };

    const admit = (user_id, record) => {
      let postdata = {
        username: user_id,
      };
      user
        .addupgradepermission(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value.splice(data.value.indexOf(record), 1);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const notadmit = (user_id, record) => {
      let postdata = {
        username: user_id,
      };
      user
        .deleteupgradepermission(postdata)
        .then((res) => {
          data.value.splice(data.value.indexOf(record), 1);
          message.success(res.data["message"]);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    let modelvisible1 = ref(false);

    let record_username = ref("");
    let isstudent = ref(false);
    let ismodel_user = ref(1);
    let enterUserInfo = (record) => {
      record_username.value = record.username;
      modelvisible1.value = true;
      if (record.usertype == "2") {
        isstudent.value = true;
      }
      ismodel_user.value = 2;
    };
    let listenuser = (val) => {
      if (val !== "") {
        ismodel_user.value = 1;
        modelvisible1.value = false;
      }
    };
    return {
      auth,
      data,
      columns,
      handleSearch,
      handleReset,
      searchInput,
      ...toRefs(state),
      // pagination,
      // current,
      loading,
      admit,
      notadmit,

      enterUserInfo,
      listenuser,
      modelvisible1,
      record_username,
      ismodel_user,
      isstudent,
      handleTableChange,
      pagination,
      OP
    };
  },
});
</script>
<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
</style>