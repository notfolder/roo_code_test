import { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient";

type Equipment = {
  id: number;
  management_number: string;
  name: string;
  category: string;
  location: string;
  status: string;
};

// 備品一覧画面（簡易表示）
export function EquipmentListPage() {
  const [items, setItems] = useState<Equipment[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await apiClient.get("/equipment");
        const data = Array.isArray(res.data) ? res.data : [];
        if (!Array.isArray(res.data)) {
          setError("取得データ形式が不正です");
        }
        setItems(data);
      } catch (err: any) {
        setError(err?.response?.data?.message || "取得に失敗しました");
        setItems([]);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>備品一覧</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>管理番号</th>
            <th>名称</th>
            <th>カテゴリ</th>
            <th>場所</th>
            <th>状態</th>
          </tr>
        </thead>
        <tbody>
          {items.map((it) => (
            <tr key={it.id}>
              <td>{it.management_number}</td>
              <td>{it.name}</td>
              <td>{it.category}</td>
              <td>{it.location}</td>
              <td>{it.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
