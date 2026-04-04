import { useState, useEffect, useCallback, FormEvent } from 'react'
import type { LoanRecord } from '../types'
import { getLoansByUser, getLoansByEquipment } from '../api/loanApi'
import { useAuth } from '../contexts/AuthContext'

export default function LoanHistoryPage() {
  const { user } = useAuth()

  // 自分の貸出履歴
  const [myLoans, setMyLoans] = useState<LoanRecord[]>([])
  const [myLoading, setMyLoading] = useState(false)
  const [myError, setMyError] = useState<string | null>(null)

  // 備品別貸出履歴（ADMIN のみ）
  const [equipmentId, setEquipmentId] = useState('')
  const [equipmentLoans, setEquipmentLoans] = useState<LoanRecord[]>([])
  const [equipmentLoading, setEquipmentLoading] = useState(false)
  const [equipmentError, setEquipmentError] = useState<string | null>(null)
  const [equipmentSearched, setEquipmentSearched] = useState(false)

  const fetchMyLoans = useCallback(async () => {
    if (!user) return
    setMyLoading(true)
    setMyError(null)
    try {
      const result = await getLoansByUser(user.id)
      // 返却日時の降順でソート（未返却は先頭）
      const sorted = [...result].sort((a, b) => {
        const aTime = a.returnedAt ? new Date(a.returnedAt).getTime() : Infinity
        const bTime = b.returnedAt ? new Date(b.returnedAt).getTime() : Infinity
        return bTime - aTime
      })
      setMyLoans(sorted)
    } catch (err: unknown) {
      setMyError(extractErrorMessage(err) ?? '貸出履歴の取得に失敗しました')
    } finally {
      setMyLoading(false)
    }
  }, [user])

  useEffect(() => { fetchMyLoans() }, [fetchMyLoans])

  const handleEquipmentSearch = async (e: FormEvent) => {
    e.preventDefault()
    if (!equipmentId.trim()) return
    setEquipmentLoading(true)
    setEquipmentError(null)
    setEquipmentSearched(true)
    try {
      const result = await getLoansByEquipment(equipmentId.trim())
      const sorted = [...result].sort((a, b) => {
        const aTime = a.returnedAt ? new Date(a.returnedAt).getTime() : Infinity
        const bTime = b.returnedAt ? new Date(b.returnedAt).getTime() : Infinity
        return bTime - aTime
      })
      setEquipmentLoans(sorted)
    } catch (err: unknown) {
      setEquipmentError(extractErrorMessage(err) ?? '貸出履歴の取得に失敗しました')
      setEquipmentLoans([])
    } finally {
      setEquipmentLoading(false)
    }
  }

  return (
    <div style={{ padding: '1.5rem', maxWidth: '900px', margin: '0 auto' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1.5rem' }}>貸出履歴</h2>

      {/* 自分の貸出履歴 */}
      <section style={sectionStyle}>
        <h3 style={sectionTitle}>自分の貸出履歴</h3>
        {myLoading && <p style={{ color: '#888', fontSize: '0.9rem' }}>読み込み中...</p>}
        {myError && <p style={errorStyle}>{myError}</p>}
        {!myLoading && !myError && myLoans.length === 0 && (
          <p style={{ color: '#888', fontSize: '0.9rem' }}>貸出履歴がありません</p>
        )}
        {!myLoading && myLoans.length > 0 && <HistoryTable loans={myLoans} />}
      </section>

      {/* 備品別貸出履歴（ADMIN のみ） */}
      {user?.role === 'ADMIN' && (
        <section style={sectionStyle}>
          <h3 style={sectionTitle}>備品別貸出履歴</h3>
          <form onSubmit={handleEquipmentSearch} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
            <input
              type="text"
              value={equipmentId}
              onChange={(e) => setEquipmentId(e.target.value)}
              placeholder="備品 ID を入力"
              style={{ ...inputStyle, flex: 1 }}
            />
            <button
              type="submit"
              style={btnStyle('#1976d2')}
              disabled={equipmentLoading || !equipmentId.trim()}
            >
              {equipmentLoading ? '検索中...' : '検索'}
            </button>
          </form>

          {equipmentError && <p style={errorStyle}>{equipmentError}</p>}
          {!equipmentLoading && equipmentSearched && !equipmentError && equipmentLoans.length === 0 && (
            <p style={{ color: '#888', fontSize: '0.9rem' }}>貸出履歴がありません</p>
          )}
          {!equipmentLoading && equipmentLoans.length > 0 && <HistoryTable loans={equipmentLoans} />}
        </section>
      )}
    </div>
  )
}

// ---- サブコンポーネント ----

function HistoryTable({ loans }: { loans: LoanRecord[] }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
      <thead>
        <tr style={{ background: '#f5f5f5' }}>
          {['備品 ID', '貸出日', '返却予定日', '返却日', 'ステータス'].map((h) => (
            <th key={h} style={thStyle}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {loans.map((loan) => (
          <tr key={loan.id} style={{ borderBottom: '1px solid #eee' }}>
            <td style={tdStyle}>{loan.equipmentId}</td>
            <td style={tdStyle}>{loan.loanDate.slice(0, 10)}</td>
            <td style={tdStyle}>{loan.dueDate.slice(0, 10)}</td>
            <td style={tdStyle}>{loan.returnedAt ? loan.returnedAt.slice(0, 10) : '—'}</td>
            <td style={tdStyle}>
              <span style={{
                display: 'inline-block',
                padding: '0.15rem 0.5rem',
                borderRadius: '12px',
                fontSize: '0.8rem',
                fontWeight: 500,
                background: loan.returnedAt ? '#e8f5e9' : '#fff3e0',
                color: loan.returnedAt ? '#2e7d32' : '#e65100',
              }}>
                {loan.returnedAt ? '返却済み' : '未返却'}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

// ---- スタイル ----

const sectionStyle: React.CSSProperties = {
  background: '#fff',
  border: '1px solid #e0e0e0',
  borderRadius: '8px',
  padding: '1.25rem',
  marginBottom: '1.5rem',
}

const sectionTitle: React.CSSProperties = {
  fontSize: '1rem',
  fontWeight: 600,
  margin: '0 0 1rem',
}

const inputStyle: React.CSSProperties = {
  padding: '0.4rem 0.6rem',
  border: '1px solid #ccc',
  borderRadius: '4px',
  width: '100%',
  boxSizing: 'border-box',
  fontSize: '0.9rem',
}

const btnStyle = (bg: string): React.CSSProperties => ({
  padding: '0.4rem 1rem',
  background: bg,
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '0.85rem',
})

const thStyle: React.CSSProperties = {
  padding: '0.5rem 0.75rem',
  textAlign: 'left',
  borderBottom: '2px solid #ddd',
  whiteSpace: 'nowrap',
}

const tdStyle: React.CSSProperties = {
  padding: '0.5rem 0.75rem',
}

const errorStyle: React.CSSProperties = {
  color: '#d32f2f',
  fontSize: '0.88rem',
  margin: '0.5rem 0',
}

// ---- ユーティリティ ----

function extractErrorMessage(err: unknown): string | null {
  if (err && typeof err === 'object') {
    const e = err as { response?: { data?: { message?: string } }; message?: string }
    return e.response?.data?.message ?? e.message ?? null
  }
  return null
}
