import { useState, useEffect, useCallback, FormEvent } from 'react'
import type { Equipment } from '../types'
import { getEquipments, searchEquipments } from '../api/equipmentApi'

const STATUS_LABEL: Record<string, string> = {
  AVAILABLE: '利用可能',
  ON_LOAN: '貸出中',
  DISPOSED: '廃棄済み',
}

const PAGE_SIZE = 20

export default function EquipmentListPage() {
  const [equipments, setEquipments] = useState<Equipment[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // フィルター状態
  const [keyword, setKeyword] = useState('')
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('')

  // 実際に検索に使うパラメータ（検索ボタン押下時に確定）
  const [appliedKeyword, setAppliedKeyword] = useState('')
  const [appliedCategory, setAppliedCategory] = useState('')
  const [appliedStatus, setAppliedStatus] = useState('')

  const isFiltered = appliedKeyword || appliedCategory || appliedStatus

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      let result
      if (isFiltered) {
        result = await searchEquipments({
          q: appliedKeyword || undefined,
          category: appliedCategory || undefined,
          status: appliedStatus || undefined,
          page,
          size: PAGE_SIZE,
        })
      } else {
        result = await getEquipments(page, PAGE_SIZE)
      }
      setEquipments(result.data)
      setTotal(result.total)
    } catch {
      setError('データの取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }, [isFiltered, appliedKeyword, appliedCategory, appliedStatus, page])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  const handleSearch = (e: FormEvent) => {
    e.preventDefault()
    setAppliedKeyword(keyword)
    setAppliedCategory(category)
    setAppliedStatus(status)
    setPage(1)
  }

  const handleReset = () => {
    setKeyword('')
    setCategory('')
    setStatus('')
    setAppliedKeyword('')
    setAppliedCategory('')
    setAppliedStatus('')
    setPage(1)
  }

  const totalPages = Math.ceil(total / PAGE_SIZE)

  return (
    <div style={{ padding: '1.5rem', maxWidth: '1100px', margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: 600 }}>備品一覧</h2>

      {/* 検索フォーム */}
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem', alignItems: 'flex-end' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <label htmlFor="keyword" style={{ fontSize: '0.8rem', color: '#555' }}>キーワード</label>
          <input
            id="keyword"
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="備品名・管理番号・カテゴリ"
            style={{ padding: '0.4rem 0.6rem', border: '1px solid #ccc', borderRadius: '4px', minWidth: '220px' }}
          />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <label htmlFor="category" style={{ fontSize: '0.8rem', color: '#555' }}>カテゴリ</label>
          <input
            id="category"
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="カテゴリ"
            style={{ padding: '0.4rem 0.6rem', border: '1px solid #ccc', borderRadius: '4px', minWidth: '140px' }}
          />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <label htmlFor="status" style={{ fontSize: '0.8rem', color: '#555' }}>ステータス</label>
          <select
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ padding: '0.4rem 0.6rem', border: '1px solid #ccc', borderRadius: '4px', minWidth: '130px' }}
          >
            <option value="">すべて</option>
            <option value="AVAILABLE">利用可能</option>
            <option value="ON_LOAN">貸出中</option>
            <option value="DISPOSED">廃棄済み</option>
          </select>
        </div>

        <button
          type="submit"
          style={{ padding: '0.4rem 1rem', background: '#1976d2', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          検索
        </button>
        <button
          type="button"
          onClick={handleReset}
          style={{ padding: '0.4rem 1rem', background: '#757575', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          リセット
        </button>
      </form>

      {error && <p style={{ color: '#d32f2f', marginBottom: '1rem' }}>{error}</p>}

      {loading ? (
        <p style={{ color: '#555' }}>読み込み中...</p>
      ) : equipments.length === 0 ? (
        <p style={{ color: '#555', padding: '2rem 0', textAlign: 'center' }}>該当する備品が見つかりません</p>
      ) : (
        <>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: '#f0f0f0' }}>
                {['備品名', '管理番号', 'カテゴリ', '数量', 'ステータス'].map((h) => (
                  <th key={h} style={{ padding: '0.6rem 0.8rem', textAlign: 'left', borderBottom: '2px solid #ddd', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {equipments.map((eq) => (
                <tr key={eq.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '0.6rem 0.8rem' }}>{eq.name}</td>
                  <td style={{ padding: '0.6rem 0.8rem' }}>{eq.assetNumber}</td>
                  <td style={{ padding: '0.6rem 0.8rem' }}>{eq.category}</td>
                  <td style={{ padding: '0.6rem 0.8rem' }}>{eq.quantity}</td>
                  <td style={{ padding: '0.6rem 0.8rem' }}>
                    <StatusBadge status={eq.status as unknown as string} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* ページネーション */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '1rem', justifyContent: 'flex-end' }}>
            <span style={{ fontSize: '0.85rem', color: '#555' }}>
              {total} 件中 {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, total)} 件表示
            </span>
            <button
              onClick={() => setPage((p) => p - 1)}
              disabled={page <= 1}
              style={{ padding: '0.3rem 0.8rem', border: '1px solid #ccc', borderRadius: '4px', cursor: page <= 1 ? 'not-allowed' : 'pointer', opacity: page <= 1 ? 0.5 : 1 }}
            >
              前へ
            </button>
            <span style={{ fontSize: '0.85rem' }}>{page} / {totalPages}</span>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={page >= totalPages}
              style={{ padding: '0.3rem 0.8rem', border: '1px solid #ccc', borderRadius: '4px', cursor: page >= totalPages ? 'not-allowed' : 'pointer', opacity: page >= totalPages ? 0.5 : 1 }}
            >
              次へ
            </button>
          </div>
        </>
      )}
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, { bg: string; color: string }> = {
    AVAILABLE: { bg: '#e8f5e9', color: '#2e7d32' },
    ON_LOAN:   { bg: '#fff3e0', color: '#e65100' },
    DISPOSED:  { bg: '#fafafa', color: '#757575' },
  }
  const style = colors[status] ?? { bg: '#f5f5f5', color: '#333' }
  return (
    <span style={{ padding: '0.2rem 0.6rem', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 500, background: style.bg, color: style.color }}>
      {STATUS_LABEL[status] ?? status}
    </span>
  )
}
