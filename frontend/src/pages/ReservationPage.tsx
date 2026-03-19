import { useState } from "react";
import { apiClient } from "../services/apiClient";

// 予約作成の簡易フォーム
export function ReservationPage() {
  const [equipmentId, setEquipmentId] = useState("");
  const [purpose, setPurpose] = useState("");
  const [startAt, setStartAt] = useState("");
  const [endAt, setEndAt] = useState("");
  const [message, setMessage] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    try {
      const res = await apiClient.post("/reservations", {
        equipment_id: Number(equipmentId),
        purpose,
        start_at: startAt,
        end_at: endAt,
      });
      setMessage(`予約完了: id=${res.data.id}`);
    } catch (err: any) {
      setMessage(err?.response?.data?.message || "失敗しました");
    }
  };

  return (
    <div>
      <h2>予約作成</h2>
      <form onSubmit={onSubmit}>
        <div>
          <label>備品ID</label>
          <input value={equipmentId} onChange={(e) => setEquipmentId(e.target.value)} required />
        </div>
        <div>
          <label>利用目的</label>
          <input value={purpose} onChange={(e) => setPurpose(e.target.value)} required />
        </div>
        <div>
          <label>開始日時</label>
          <input type="datetime-local" value={startAt} onChange={(e) => setStartAt(e.target.value)} required />
        </div>
        <div>
          <label>終了日時</label>
          <input type="datetime-local" value={endAt} onChange={(e) => setEndAt(e.target.value)} required />
        </div>
        <button type="submit">予約する</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
