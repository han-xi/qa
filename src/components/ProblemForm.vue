<template>
  <a-form
    ref="formRef"
    v-bind="formItemLayoutWithOutLabel"
    :model="dynamicValidateForm"
  >
    <a-form-item
      has-feedback
      label="问题"
      name="question"
      v-bind="formItemLayout"
      :rules="{
        required: true,
        message: '问题不能为空',
        trigger: 'change',
      }"
    >
      <a-input
        placeholder="请输入问题"
        v-model:value="dynamicValidateForm.question"
      />
    </a-form-item>
    <a-form-item
      v-for="(domain, index) in dynamicValidateForm.domains"
      :key="domain.key"
      v-bind="formItemLayout"
      :label="domain.num"
      :name="['domains', index, 'value']"
      :rules="{
        required: true,
        message: '选项不能为空',
        trigger: 'change',
      }"
    >
      <a-input
        v-model:value="domain.value"
        placeholder="请输入选项"
        style="width: 60%; margin-right: 8px"
      />
      <MinusCircleOutlined
        class="dynamic-delete-button"
        v-if="index === dynamicValidateForm.domains.length - 1 && index > 0"
        @click="removeDomain(domain)"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button
        type="dashed"
        style="width: 60%"
        @click="addDomain"
        v-if="dynamicValidateForm.domains.length < 6"
      >
        <PlusOutlined />
        增加选项
      </a-button>
    </a-form-item>
    <a-form-item
      v-for="(tag, index) in dynamicValidateForm.tags"
      :key="tag.key"
      v-bind="formItemLayout"
      :label="tag.num"
      :name="['tag', index, 'value']"
    >
      <a-input
        v-model:value="tag.value"
        placeholder="请输入标签"
        style="width: 60%; margin-right: 8px"
      />
      <MinusCircleOutlined
        class="dynamic-delete-button"
        v-if="index === dynamicValidateForm.tags.length - 1"
        @click="removeTag(tag)"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button
        type="dashed"
        style="width: 60%"
        @click="addTag"
        v-if="dynamicValidateForm.tags.length < 6"
      >
        <PlusOutlined />
        增加标签
      </a-button>
    </a-form-item>
    <a-form-item
      has-feedback
      label="答案"
      name="answer"
      ref="name"
      v-bind="formItemLayout"
      :autoLink="false"
      :rules="{
        required: true,
        message: '选择答案',
      }"
    >
      <a-select
        v-model:value="dynamicValidateForm.answer"
        placeholder="选择答案"
        :options="options"
        @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
        @change="
          () => {
            $refs.name.onFieldChange();
          }
        "
      >
      </a-select
    ></a-form-item>
    <a-form-item
      has-feedback
      label="插入题库"
      name="checkedList"
      ref="name"
      v-bind="formItemLayout"
      :autoLink="false"
      :rules="{
        required: true,
        message: '选择班级',
      }"
    >
      <div :style="{ borderBottom: '1px solid #E9E9E9' }">
        <a-checkbox
          v-model:checked="checkAll"
          :indeterminate="indeterminate"
          @change="onCheckAllChange"
        >
          全选
        </a-checkbox>
      </div>
      <br />
      <a-checkbox-group
        v-model:value="dynamicValidateForm.checkedList"
        @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
        @change="
          () => {
            $refs.name.onFieldChange();
          }
        "
        :options="plainOptions"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayoutWithOutLabel">
      <a-button
        type="primary"
        html-type="submit"
        :loading="loading"
        @click="submitForm"
        >提交</a-button
      >
      <a-button style="margin-left: 10px" @click="resetForm">重置</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons-vue";
import { defineComponent, reactive, ref, watch, toRefs } from "vue";
import question from "../apis/question";
import { message } from "ant-design-vue";
export default defineComponent({
  name: "ProblemForm",
  setup() {
    const formRef = ref();
    const formItemLayout = {
      labelCol: {
        xs: {
          span: 24,
        },
        sm: {
          span: 4,
        },
      },
      wrapperCol: {
        xs: {
          span: 24,
        },
        sm: {
          span: 20,
        },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 20,
          offset: 4,
        },
      },
    };
    const dynamicValidateForm = reactive({
      domains: [
        { value: "", key: Date.now(), num: "A" },
        { value: "", key: Date.now(), num: "B" },
        { value: "", key: Date.now(), num: "C" },
        { value: "", key: Date.now(), num: "D" },
      ],
      tags: [],
      answer: undefined,
      question: "",
      checkedList: [],
    });
    let loading = ref(false);
    const submitForm = () => {
      console.log(dynamicValidateForm);
      formRef.value
        .validate()
        .then(() => {
          let class_id = dynamicValidateForm.checkedList.toString();

          let ops = new Array();
          let tags = new Array();
          dynamicValidateForm.domains.forEach((Element) => {
            ops.push(Element.value);
          });
          ops = ops.toString();
          dynamicValidateForm.tags.forEach((Element) => {
            tags.push(Element.value);
          });
          tags = tags.toString();
          let postdata = {
            class_id: class_id,
            tags: tags,
            problem: dynamicValidateForm.question,
            answer: dynamicValidateForm.answer,
            options: ops,
          };
          loading.value = true;
          question
            .addquestion(postdata)
            .then((res) => {
              message.success(res.data["message"]);
              loading.value = false;
            })
            .catch((err) => {
              loading.value = false;
              message.error(err.data["message"]);
            });
        })
        .catch((error) => {
          console.log("error", error);
        });
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };

    const removeDomain = (item) => {
      let index = dynamicValidateForm.domains.indexOf(item);

      if (index !== -1) {
        dynamicValidateForm.domains.splice(index, 1);
        options.value.splice(index, 1);
      }
    };
    const removeTag = (item) => {
      let index = dynamicValidateForm.tags.indexOf(item);

      if (index !== -1) {
        dynamicValidateForm.tags.splice(index, 1);
      }
    };
    let options = ref([
      { value: 1, label: "A" },
      { value: 2, label: "B" },
      { value: 3, label: "C" },
      { value: 4, label: "D" },
    ]);
    const addDomain = () => {
      dynamicValidateForm.domains.push({
        value: "",
        key: Date.now(),
        num: String.fromCharCode(
          "A".charCodeAt(0) + dynamicValidateForm.domains.length
        ),
      });
      options.value.push({
        value: dynamicValidateForm.domains.length,
        label: String.fromCharCode(
          "A".charCodeAt(0) + dynamicValidateForm.domains.length - 1
        ),
      });
    };
    const addTag = () => {
      dynamicValidateForm.tags.push({
        value: "",
        key: Date.now(),
        num: String.fromCharCode(
          "1".charCodeAt(0) + dynamicValidateForm.tags.length
        ),
      });
    };
    let plainOptions = ref(["default"]);
    const state = reactive({
      indeterminate: true,
      checkAll: false,
      //   checkedList: ['Apple', 'Orange'],
    });

    const onCheckAllChange = (e) => {
      Object.assign(state, {
        //    checkedList: e.target.checked ? plainOptions.value : [],
        indeterminate: false,
      });
      Object.assign(dynamicValidateForm, {
        checkedList: e.target.checked ? plainOptions.value : [],
        // indeterminate: false,
      });
    };

    watch(
      () => dynamicValidateForm.checkedList,
      (val) => {
        state.indeterminate =
          !!val.length && val.length < plainOptions.value.length;
        state.checkAll = val.length === plainOptions.value.length;
      }
    );
    return {
      formRef,
      formItemLayout,
      formItemLayoutWithOutLabel,
      dynamicValidateForm,
      submitForm,
      resetForm,
      removeDomain,
      removeTag,
      addDomain,
      addTag,
      options,
      ...toRefs(state),
      plainOptions,
      onCheckAllChange,
      loading,
    };
  },

  components: {
    MinusCircleOutlined,
    PlusOutlined,
  },
});
</script>
<style>
.dynamic-delete-button {
  cursor: pointer;
  position: relative;
  top: 4px;
  font-size: 24px;
  color: #999;
  transition: all 0.3s;
}
.dynamic-delete-button:hover {
  color: #777;
}
.dynamic-delete-button[disabled] {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>