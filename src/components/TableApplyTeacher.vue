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
            <a @click="enterUserInfo(record)" :key="i">{{ fragment }}</a>
          </template>
        </template>
      </span>
      <template v-else>
        <a @click="enterUserInfo(record)">{{ text }}</a>
      </template>
    </template>
    <template #customRender1="{ text, column, record }">
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
            <a @click="enterClassInfo(record)" :key="i">{{ fragment }}</a>
          </mark>
          <template v-else>
            <a @click="enterClassInfo(record)" :key="i">{{ fragment }}</a>
          </template>
        </template>
      </span>
      <template v-else>
        <a @click="enterClassInfo(record)">{{ text }}</a>
      </template>
    </template>
    <template #admit="{ record }">
      <a-button
        type="primary"
        @click="admit(record.class_id, record.username, record)"
        :disabled="record.isoperated"
        >准许</a-button
      >
    </template>
    <template #notadmit="{ record }">
      <a-button
        type="primary"
        @click="notadmit(record.class_id, record.username, record)"
        :disabled="record.isoperated"
        >驳回</a-button
      >
    </template>
  </a-table>
  <student-info
    :ismodel="ismodel_user"
    :visible="modelvisible1"
    :isstudent="false"
    :class_id="record_class_id"
    :user_id="record_username"
    @listen="listenuser"
  ></student-info>
  <class-info
    :ismodel="ismodel_class"
    :visible="modelvisible"
    :class_id="record_class_id"
    @listen="listenclass"
  ></class-info>
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
import classes from "../apis/classes";
import auth from "../auth";
import ClassInfo from "../components/ClassInfo.vue";
import StudentInfo from "../components/StudentInfo.vue";
export default defineComponent({
  components: {
    SearchOutlined,
    ClassInfo,
    StudentInfo,
  },
  name: "TableApplyTeacher",
  setup() {
    let loading = ref(true);
    let total = ref(0);
    const data = ref([]);
    let current = ref(1);
    let sorterOrder = ref("");

    onBeforeMount(() => {
      getapplyteacherlist();
    });
    const getapplyteacherlist = () => {
      const postdata = {
        current: current.value,
        sorter: sorterOrder.value,

        search: state.searchText,
        search1: state.searchText1,
      };
      classes
        .getapplyteacherlist(postdata)
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
        title: "班级",
        dataIndex: "class_name",
        key: "class_name",
        slots: {
          filterDropdown: "filterDropdown",
          filterIcon: "filterIcon",
          customRender: "customRender1",
        },
        onFilter: (value, record) =>
          record.class_name
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
        //  (a, b) =>
        //   convertDateFromString(a.updatetime) -
        //   convertDateFromString(b.updatetime),
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
      pageSize: 2,
    }));

    const handleTableChange = (pag, filters, sorter) => {
      (current.value = pag.current), (sorterOrder.value = sorter.order);
      getapplyteacherlist();
      console.log(sorterOrder.value);
    };
    const handleSearch = (selectedKeys, confirm, dataIndex) => {
      confirm();
      current.value = 1;
      if (dataIndex == "class_name") {
        state.searchText1 = selectedKeys[0];
        state.searchedColumn1 = dataIndex;
      } else {
        state.searchText = selectedKeys[0];
        state.searchedColumn = dataIndex;
      }
      getapplyteacherlist();
    };

    const handleReset = (clearFilters, dataIndex) => {
      clearFilters();
      if (dataIndex == "class_name") {
        state.searchText1 = "";
        state.searchedColumn1 = "";
      } else {
        state.searchText = "";
        state.searchedColumn = "";
      }

      getapplyteacherlist();
    };

    const admit = (class_id, user_id, record) => {
      let postdata = {
        class_id: class_id,
        user_id: user_id,
      };
      classes
        .addteacher(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value.splice(data.value.indexOf(record), 1);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const notadmit = (class_id, user_id, record) => {
      let postdata = {
        class_id: class_id,
        user_id: user_id,
        type: "notadmit",
      };
      classes
        .deleteteacher(postdata)
        .then((res) => {
          data.value.splice(data.value.indexOf(record), 1);
          message.success(res.data["message"]);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    let modelvisible = ref(false);
    let modelvisible1 = ref(false);
    let record_class_id = ref("");
    let record_username = ref("");
    let ismodel_class = ref(1);
    let ismodel_user = ref(1);
    let enterClassInfo = (record) => {
      record_class_id.value = record.class_id;
      ismodel_class.value = 2;
      modelvisible.value = true;
    };
    let enterUserInfo = (record) => {
      record_username.value = record.username;
      record_class_id.value = record.class_id;
      ismodel_user.value = 2;
      modelvisible1.value = true;
    };
    let listenclass = (val) => {
      if (val !== "") {
        ismodel_class.value = 1;
        modelvisible.value = false;
      }
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
      enterClassInfo,
      listenclass,
      modelvisible,
      enterUserInfo,
      listenuser,
      modelvisible1,
      record_class_id,
      record_username,
      ismodel_class,
      ismodel_user,
      handleTableChange,
      pagination,
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