<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])
const form = reactive({
  email: '',
  password: ''
})

const submit = () => {
  emit('submit', { ...form })
}
</script>

<template>
  <v-card class="mx-auto" max-width="480" elevation="6">
    <v-card-title class="text-h6 py-4">備品貸出システムへログイン</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="form.email"
          label="メールアドレス"
          type="email"
          variant="outlined"
          data-testid="login-email"
          required
        />
        <v-text-field
          v-model="form.password"
          label="パスワード"
          type="password"
          variant="outlined"
          data-testid="login-password"
          required
        />
        <v-btn block type="submit" color="primary" data-testid="login-submit">ログイン</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
