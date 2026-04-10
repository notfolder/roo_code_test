<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="mb-4">
          <v-card-title>ユーザー登録</v-card-title>
          <v-card-text>
            <v-form ref="createForm">
              <v-text-field v-model="form.name" label="氏名" required />
              <v-text-field v-model="form.email" label="メールアドレス" required />
              <v-text-field v-model="form.password" label="パスワード" type="password" required />
            </v-form>
            <v-alert v-if="createError" type="error" dense>{{ createError }}</v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="registerUser">追加</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-card>
      <v-card-title>ユーザー一覧</v-card-title>
      <v-card-text>
        <v-data-table :items="users" :headers="headers" dense>
          <template #item.actions="{ item }">
            <v-btn text small color="primary" @click="editUser(item)">編集</v-btn>
            <v-btn text small color="error" @click="removeUser(item)">削除</v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-dialog v-model="editDialog" persistent max-width="450">
      <v-card>
        <v-card-title>ユーザー編集</v-card-title>
        <v-card-text>
          <v-text-field v-model="editForm.name" label="氏名" />
          <v-text-field v-model="editForm.email" label="メール" />
          <v-alert v-if="editError" type="error" dense>{{ editError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="editDialog = false">キャンセル</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="submitEdit">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { createUser, deleteUser, listUsers, updateUser } from "../services/api";

const users = ref([]);
const headers = [
  { title: "氏名", value: "name" },
  { title: "メール", value: "email" },
  { title: "ステータス", value: "status" },
  { title: "操作", value: "actions", sortable: false },
];

const form = reactive({ name: "", email: "", password: "" });
const createError = ref("");
const editDialog = ref(false);
const editForm = reactive({ id: "", name: "", email: "" });
const editError = ref("");

const loadUsers = async () => {
  users.value = await listUsers();
};

const registerUser = async () => {
  try {
    await createUser(form);
    form.name = "";
    form.email = "";
    form.password = "";
    createError.value = "";
    await loadUsers();
  } catch (err) {
    createError.value = err.message;
  }
};

const editUser = (user) => {
  editForm.id = user.id;
  editForm.name = user.name;
  editForm.email = user.email;
  editError.value = "";
  editDialog.value = true;
};

const submitEdit = async () => {
  try {
    await updateUser(editForm.id, { name: editForm.name, email: editForm.email });
    editDialog.value = false;
    await loadUsers();
  } catch (err) {
    editError.value = err.message;
  }
};

const removeUser = async (user) => {
  await deleteUser(user.id);
  await loadUsers();
};

onMounted(() => {
  loadUsers();
});
</script>
