import { useState } from "react";
import { apiClient } from "../services/apiClient";

// ログイン画面（簡易）
export function LoginPage() {
  const [loginId, setLoginId] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    try {
      const res = await apiClient.post("/auth/login", { login_id: loginId, password });
      setMessage(`ログイン成功: token=${res.data.token}`);
      localStorage.setItem("token", res.data.token);
    } catch (err: any) {
      setMessage(err?.response?.data?.message || "ログイン失敗");
    }
  };

  return (
    <div>
      <h2>ログイン</h2>
      <form onSubmit={onSubmit}>
        <div>
          <label>ログインID</label>
          <input value={loginId} onChange={(e) => setLoginId(e.target.value)} required />
        </div>
        <div>
          <label>パスワード</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">ログイン</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
