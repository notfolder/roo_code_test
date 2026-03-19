import { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient";

type Reservation = {
  id: number;
  equipment_id: number;
  start_at: string;
  end_at: string;
  status: string;
};

// 空き状況（シンプルな予約一覧）
export function AvailabilityPage() {
  const [items, setItems] = useState<Reservation[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await apiClient.get("/reservations");
        setItems(res.data);
      } catch (err: any) {
        setError(err?.response?.data?.message || "取得に失敗しました");
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>空き状況（予約一覧）</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {items.map((r) => (
          <li key={r.id}>
            #{r.id} equip:{r.equipment_id} {r.start_at} - {r.end_at} [{r.status}]
          </li>
        ))}
      </ul>
    </div>
  );
}
