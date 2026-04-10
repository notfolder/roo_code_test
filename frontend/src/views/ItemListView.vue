<template>
  <v-container>
    <v-card class="mt-6">
      <v-card-title>備品一覧</v-card-title>
      <v-card-text>
        <v-data-table
          :items="items"
          :headers="headers"
          item-value="id"
          :loading="loading"
        >
          <template #item.operating="{ item }">
            <v-btn small color="primary" text @click="openLoan(item)" :disabled="item.state === 'lent'">
              貸出
            </v-btn>
            <v-btn small color="info" text @click="returnItem(item)" :disabled="item.state === 'available'">
              返却
            </v-btn>
            <v-btn small color="secondary" text @click="editItem(item)">
              編集
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="openForm">備品登録</v-btn>
        <v-spacer />
      </v-card-actions>
    </v-card>

    <v-dialog v-model="formDialog" persistent max-width="500">
      <v-card>
        <v-card-title>{{ editingItem ? "備品編集" : "備品登録" }}</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field v-model="form.asset_number" label="資産管理番号" required :disabled="Boolean(editingItem)" />
            <v-text-field v-model="form.name" label="名称" required />
            <v-select
              v-model="form.state"
              :items="states"
              item-title="label"
              item-value="value"
              label="状態"
              required
            />
          </v-form>
          <v-alert v-if="formError" type="error" dense>{{ formError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeForm">キャンセル</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="submitForm">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="loanDialog" persistent max-width="420">
      <v-card>
        <v-card-title>貸出処理</v-card-title>
        <v-card-text>
          <div class="mb-2">{{ loanTarget?.asset_number }} / {{ loanTarget?.name }}</div>
          <v-select
            v-model="loanPayload.user_id"
            :items="users"
            item-title="name"
            item-value="id"
            label="貸出先社員"
            required
          />
          <v-alert v-if="loanError" type="error" dense>{{ loanError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="loanDialog = false">キャンセル</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="confirmLoan">貸出を確定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import {
  createItem,
  listItems,
  listUsers,
  loanItem,
  returnItem as returnPayload,
  updateItem,
} from "../services/api";

const items = ref([]);
const users = ref([]);
const headers = [
  { title: "資産番号", value: "asset_number" },
  { title: "名称", value: "name" },
  { title: "状態", value: "state" },
  { title: "貸出先", value: "current_user_name" },
  { title: "操作", value: "operating", sortable: false },
];

const loading = ref(false);
const formDialog = ref(false);
const formRef = ref(null);
const editingItem = ref(null);
const loanDialog = ref(false);
const loanTarget = ref(null);
const loanPayload = reactive({ user_id: "" });
const form = reactive({ asset_number: "", name: "", state: "available" });
const formError = ref("");
const loanError = ref("");
const states = [
  { label: "貸出可", value: "available" },
  { label: "貸出中", value: "lent" },
];

const refresh = async () => {
  loading.value = true;
  try {
    items.value = await listItems();
    users.value = await listUsers();
    loanPayload.user_id = "";
  } finally {
    loading.value = false;
  }
};

const openForm = () => {
  editingItem.value = null;
  form.asset_number = "";
  form.name = "";
  form.state = "available";
  formError.value = "";
  formDialog.value = true;
};

const editItem = (item) => {
  editingItem.value = item;
  form.asset_number = item.asset_number;
  form.name = item.name;
  form.state = item.state;
  formError.value = "";
  formDialog.value = true;
};

const closeForm = () => {
  formDialog.value = false;
};

const submitForm = async () => {
  try {
    if (editingItem.value) {
      await updateItem(editingItem.value.id, { name: form.name, state: form.state });
    } else {
      await createItem({ asset_number: form.asset_number, name: form.name, state: form.state });
    }
    formDialog.value = false;
    await refresh();
  } catch (err) {
    formError.value = err.message;
  }
};

const openLoan = (item) => {
  loanTarget.value = item;
  loanPayload.user_id = "";
  loanError.value = "";
  loanDialog.value = true;
};

const confirmLoan = async () => {
  try {
    await loanItem(loanTarget.value.id, { user_id: loanPayload.user_id });
    loanDialog.value = false;
    await refresh();
  } catch (err) {
    loanError.value = err.message;
  }
};

const returnItem = async (item) => {
  try {
    await returnPayload(item.id);
  } catch (err) {
    loanError.value = err.message;
  }
  await refresh();
};

onMounted(() => {
  refresh();
});
</script>
