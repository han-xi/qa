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
            <router-link :key="i" :to="`/classlist/classinfo/${record.key}`">{{
              fragment
            }}</router-link>
          </mark>
          <template v-else>
            <router-link :key="i" :to="`/classlist/classinfo/${record.key}`">{{
              fragment
            }}</router-link></template
          >
        </template>
      </span>
      <template v-else>
        <router-link :to="`/classlist/classinfo/${record.key}`">
          {{ text }}</router-link
        >
      </template>
    </template>
    <template #enterclass="{ record }">
      <a-button
        v-if="
          (record.isstudent && auth.user.usertype == 1) ||
          (record.isteacher && auth.user.usertype == 2) ||
          auth.user.usertype > 2
        "
        type="primary"
        @click="enterClass(record.key, record.name)"
        >进入</a-button
      >

      <a-button v-else type="primary" :disabled="true">无权限</a-button>
    </template>
    <template #applystudent="{ record }">
      <a-button
        v-if="!record.isstudent && !record.isstudentapply"
        type="primary"
        @click="applyClass(record.key, record)"
        >点击申请</a-button
      >
      <a-button
        v-else-if="record.isstudentapply"
        type="primary"
        :disabled="true"
        >待审核</a-button
      >
      <a-button v-else type="primary" :disabled="true">已加入</a-button>
    </template>
    <template #quitstudent="{ record }">
      <a-popconfirm
        v-if="record.isstudent"
        :title="`确认要退出${record.name}?`"
        ok-text="退出"
        cancel-text="取消"
        @confirm="quitstudent(record.key, record)"
      >
        <a-button type="primary">退出</a-button>
      </a-popconfirm>

      <a-button v-else type="primary" :disabled="true">请先申请</a-button>
    </template>

    <template #quitteacher="{ record }">
      <a-popconfirm
        v-if="record.isteacher"
        :title="`确认要退出${record.name}?`"
        ok-text="退出"
        cancel-text="取消"
        @confirm="quitteacher(record.key, record)"
      >
        <a-button type="primary">退出</a-button>
      </a-popconfirm>
      <a-button v-else type="primary" :disabled="true">请先申请</a-button>
    </template>
    <template #applyteacher="{ record }" v-if="auth.user.usertype > 1">
      <a-button
        type="primary"
        v-if="!record.isteacher && !record.isteacherapply"
        @click="applyTeacher(record.key, record)"
        >点击申请</a-button
      >
      <a-button
        type="primary"
        v-else-if="record.isteacherapply"
        :disabled="true"
        >待审核</a-button
      >
      <a-button v-else type="primary" :disabled="true">已加入</a-button>
    </template>

        <template #deleteclass="{ record }" v-if="auth.user.usertype > 2">
  <a-popconfirm
        :title="`确认要删除${record.name}?`"
        ok-text="删除"
        cancel-text="取消"
        @confirm="deleteclass(record.key, record)"
      >
        <a-button type="primary">删除</a-button>
      </a-popconfirm>
    </template>
  </a-table>
</template>
<script>
import { SearchOutlined } from "@ant-design/icons-vue";
import {
  onMounted,
  defineComponent,
  reactive,
  ref,
  toRefs,
  computed,
} from "vue";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import classes from "../apis/classes";
import auth from "../auth";
export default defineComponent({
  components: {
    SearchOutlined,
  },
  name: "TableQeustionChange",
  setup() {
    let loading = ref(true);
    // let current = ref(1);
    // let pageSize = ref(5);
    let total = ref(0);
    const data = ref([]);
    let current = ref(1);
    let sorterOrder = ref("");
    onMounted(() => {
      getclasslist();
    });
    const getclasslist = () => {
      const postdata = {
        user_id: localStorage.getItem("username"),
        current: current.value,
        sorter: sorterOrder.value,
        search: state.searchText,
      };
      classes
        .getclasslist(postdata)
        .then((res) => {
          data.value = res.data["result"];
          total.value = res.data["total"];
          // total.value = data.value.length;
          loading.value = false;
        })
        .catch((error) => {
          console.log(error);
          loading.value = false;
        });
    };
    const state = reactive({
      searchText: "",
      searchedColumn: "",
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
    let columns = [
      {
        title: "Name",
        dataIndex: "name",
        key: "name",
        slots: {
          filterDropdown: "filterDropdown",
          filterIcon: "filterIcon",
          customRender: "customRender",
        },
        onFilter: (value, record) =>
          record.name.toString().toLowerCase().includes(value.toLowerCase()),
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
        title: "注册时间",
        dataIndex: "registertime",
        key: "registertime",
        sorter: true,
        // (a, b) =>
        //   convertDateFromString(a.registertime) -
        //   convertDateFromString(b.registertime),
        sortDirections: ["descend", "ascend"],
      },
      {
        title: "查看学生",
        slots: { customRender: "enterclass" },
      },
      {
        title: "申请加入",
        slots: { customRender: "applystudent" },
      },
      {
        title: "退出班级",
        slots: { customRender: "quitstudent" },
      },
      {
        title: "取消任职",
        slots: { customRender: "quitteacher" },
      },
      {
        title: "申请代课",
        slots: { customRender: "applyteacher" },
      },
      {
        title: "删除班级",
        slots: { customRender: "deleteclass" },
      },
    ];

    if (auth.user.usertype == 1) {
      columns = columns.filter(
        (item) =>
          item.title !== "申请代课" &&
          item.title !== "取消任职" &&
          item.title !== "删除班级"
      );
    } else if (auth.user.usertype == 3) {
      columns = columns.filter(
        (item) =>
          item.title !== "申请代课" &&
          item.title !== "申请加入" &&
          item.title !== "退出班级" &&
          item.title !== "取消任职" 
      );
    } else if (auth.user.usertype == 2) {
      columns = columns.filter(
        (item) => item.title !== "申请加入" && item.title !== "退出班级"&&
          item.title !== "删除班级"
      );
    }
    const pagination = computed(() => ({
      total: total.value,
      current: current.value,
      pageSize: 2,
    }));

    const handleTableChange = (pag, filters, sorter) => {
      (current.value = pag.current), (sorterOrder.value = sorter.order);
      getclasslist();
      console.log(sorterOrder.value);
    };
    const handleSearch = (selectedKeys, confirm, dataIndex) => {
      // console.log(dataIndex)
      confirm();
      current.value = 1;
      state.searchText = selectedKeys[0];
      state.searchedColumn = dataIndex;

      getclasslist();
    };

    const handleReset = (clearFilters) => {
      clearFilters();
      state.searchText = "";
      getclasslist();
    };
    const router = useRouter();
    const enterClass = (key, name) => {
      // console.log(ke);
      router.push({ path: `/classlist/class/${key}/${name}` });
    };

    const applyClass = (key, record) => {
      let postdata = {
        class_id: key,
      };
      classes
        .applystudent(postdata)
        .then((res) => {
          message.success(res.data["message"]);

          data.value[data.value.indexOf(record)].isstudentapply = true;
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const applyTeacher = (key, record) => {
      let postdata = {
        class_id: key,
      };
      classes
        .applyteacher(postdata)
        .then((res) => {
          message.success(res.data["message"]);

          data.value[data.value.indexOf(record)].isteacherapply = true;
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const quitstudent = (key, record) => {
      let postdata = {
        class_id: key,
        type: "delete",
      };
      classes
        .deletestudent(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value[data.value.indexOf(record)].isstudent = false;
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const quitteacher = (key, record) => {
      let postdata = {
        class_id: key,
        type: "delete",
      };
      classes
        .deleteteacher(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value[data.value.indexOf(record)].isteacher = false;
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    const deleteclass =(key, record) => {
      let postdata = {
        type: "delete",
        class_id: key,
      };
      classes
        .deleteclass(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value.splice(data.value.indexOf(record), 1);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    return {
      auth,
      data,
      columns,
      handleSearch,
      handleReset,
      searchInput,
      ...toRefs(state),
      enterClass,
      // pagination,
      // current,
      loading,
      applyClass,
      applyTeacher,
      quitstudent,
      quitteacher,
      handleTableChange,
      pagination,
      deleteclass
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