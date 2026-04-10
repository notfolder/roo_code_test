<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>備品貸出システム ログイン</v-card-title>
          <v-card-text>
            <v-form ref="formRef" v-model="valid" lazy-validation>
              <v-text-field
                label="メールアドレス"
                v-model="credentials.email"
                type="email"
                :rules="[required]"
                :input-props="{ 'data-testid': 'email-input' }"
              />
              <v-text-field
                label="パスワード"
                v-model="credentials.password"
                type="password"
                :rules="[required]"
                :input-props="{ 'data-testid': 'password-input' }"
              />
            </v-form>
            <v-alert v-if="error" type="error" dense>
              {{ error }}
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" :disabled="loading" @click="onSubmit">
              {{ loading ? "認証中..." : "ログイン" }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../services/api";

const router = useRouter();
const credentials = reactive({ email: "", password: "" });
const valid = ref(false);
const error = ref("");
const loading = ref(false);
const formRef = ref(null);

const required = (value) => !!value || "必須項目です";

const onSubmit = async () => {
  if (!formRef.value?.validate()) {
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    const data = await login(credentials);
    localStorage.setItem("asset_token", data.access_token);
    localStorage.setItem("asset_role", data.role);
    localStorage.setItem("asset_user", data.user_id);
    router.push("/items");
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>
