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
            <router-link
              :key="i"
              :to="`/classlist/class/${class_id}/${classname}/studentinfo/${record.name}`"
            >
              {{ fragment }}</router-link
            >
          </mark>
          <template v-else>
            <router-link
              :key="i"
              :to="`/classlist/class/${class_id}/${classname}/studentinfo/${record.name}`"
              >{{ fragment }}</router-link
            ></template
          >
        </template>
      </span>
      <template v-else>
        <router-link
          :to="`/classlist/class/${class_id}/${classname}/studentinfo/${record.name}`"
        >
          {{ text }}</router-link
        >
      </template>
    </template>
    <template #operation="{ record }">
      <a-button type="primary" @click="enterStudent(record.key)"
        >查看错题</a-button
      >
    </template>
    <template #deletestudent="{ record }">
      <a-popconfirm
        :title="`确认要删除${record.key}?`"
        ok-text="删除"
        cancel-text="取消"
        @confirm="deletestudent(record.key, record)"
      >
        <a-button type="primary">删除</a-button>
      </a-popconfirm>
    </template>
  </a-table>
</template>
<script>
import { SearchOutlined } from "@ant-design/icons-vue";
import { defineComponent, reactive, ref, toRefs, onBeforeMount,computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import classes from "../apis/classes";
import { message } from "ant-design-vue";
import auth from "../auth";
export default defineComponent({
  components: {
    SearchOutlined,
  },
  name: "TableSearchStudent",
  setup() {
    const router = useRouter();
    const route = useRoute();
    let loading = ref(true);
    // let current = ref(1);

    let total = ref(0);
    let current = ref(1)
    let sorterOrder =ref('')
    const data = ref([]);
    onBeforeMount(() => {
      getstudentlist();
    });
    const getstudentlist = () => {
      const postdata = {
        class_id: route.params.cid,
        current:current.value,
        sorter:sorterOrder.value,
        search: state.searchText        
      };
      classes
        .getstudentlist(postdata)
        .then((res) => {
          data.value = res.data["result"];
         total.value =res.data["total"]
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
        title: "学生名",
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
              console.log(searchInput.value);
              searchInput.value.focus();
            }, 100);
          }
        },
      },
      {
        title: "加入时间",
        dataIndex: "registertime",
        key: "registertime",
        sorter: true,
        // (a, b) =>
        //   convertDateFromString(a.registertime) -
        //   convertDateFromString(b.registertime),
        sortDirections: ["descend", "ascend"],
      },
      {
        title: "查看错题",

        slots: { customRender: "operation" },
      },
      {
        title: "删除学生",

        slots: { customRender: "deletestudent" },
      },
    ];
    if (auth.user.usertype == 1) {
      columns = columns.filter((item) => item.title !== "删除学生"&&item.title!=="查看错题");
    }
   const handleTableChange = (pag, filters, sorter) => {

        current.value= pag.current,
         
        sorterOrder.value= sorter.order
        getstudentlist()
        console.log(sorterOrder.value)
    }
    const handleSearch = (selectedKeys, confirm, dataIndex) => {
      confirm();
       current.value=1
      state.searchText = selectedKeys[0];
      state.searchedColumn = dataIndex;
      getstudentlist()
      // selectedKeys[0] = state.searchText
    };
    const pagination = computed(() => ({
      total: total.value,
      current: current.value,
      pageSize: 2,
    }));
    const handleReset = (clearFilters) => {
      clearFilters();
      state.searchText = "";
      getstudentlist()
    };

    const class_id = ref("");
    const classname = ref("");
    class_id.value = route.params.cid;
    classname.value = route.params.cname;
    const enterStudent = (val) => {
      router.push("/classlist/class/"+class_id.value+"/"+classname.value+"/"+"studentwrongquestion/" + val);
    };
    const deletestudent = (user_id, record) => {
      let postdata = {
        user_id: user_id,
        type: "delete",
        class_id: class_id.value,
      };
      classes
        .deletestudent(postdata)
        .then((res) => {
          message.success(res.data["message"]);
          data.value.splice(data.value.indexOf(record), 1);
        })
        .catch((error) => {
          message.error(error.data["message"]);
        });
    };
    return {
      data,
      columns,
      handleSearch,
      handleReset,
      searchInput,
      ...toRefs(state),
      enterStudent,
      class_id,
      loading,
      getstudentlist,
      classname,
      deletestudent,
     handleTableChange,
      pagination
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