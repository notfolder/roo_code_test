import { useState, useEffect, useCallback, FormEvent } from 'react'
import type { Equipment } from '../types'
import { getEquipments, createEquipment, updateEquipment, disposeEquipment } from '../api/equipmentApi'

const STATUS_LABEL: Record<string, string> = {
  AVAILABLE: '利用可能',
  ON_LOAN: '貸出中',
  DISPOSED: '廃棄済み',
}

const PAGE_SIZE = 20

interface EquipmentForm {
  assetNumber: string
  name: string
  category: string
  quantity: string
}

const emptyForm = (): EquipmentForm => ({ assetNumber: '', name: '', category: '', quantity: '1' })

export default function EquipmentManagePage() {
  const [equipments, setEquipments] = useState<Equipment[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 登録フォーム
  const [showCreate, setShowCreate] = useState(false)
  const [createForm, setCreateForm] = useState<EquipmentForm>(emptyForm())
  const [createError, setCreateError] = useState<string | null>(null)
  const [createLoading, setCreateLoading] = useState(false)

  // 編集フォーム
  const [editTarget, setEditTarget] = useState<Equipment | null>(null)
  const [editForm, setEditForm] = useState<Omit<EquipmentForm, 'assetNumber'>>({ name: '', category: '', quantity: '1' })
  const [editError, setEditError] = useState<string | null>(null)
  const [editLoading, setEditLoading] = useState(false)

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getEquipments(page, PAGE_SIZE)
      setEquipments(result.data)
      setTotal(result.total)
    } catch {
      setError('データの取得に失敗しました')
    } finally {
      setLoading(false)
    }
  }, [page])

  useEffect(() => { fetchData() }, [fetchData])

  // 登録
  const handleCreate = async (e: FormEvent) => {
    e.preventDefault()
    setCreateError(null)
    setCreateLoading(true)
    try {
      await createEquipment({
        assetNumber: createForm.assetNumber.trim(),
        name: createForm.name.trim(),
        category: createForm.category.trim(),
        quantity: Number(createForm.quantity),
      })
      setShowCreate(false)
      setCreateForm(emptyForm())
      setPage(1)
      await fetchData()
    } catch (err: unknown) {
      const msg = extractErrorMessage(err)
      setCreateError(msg ?? '登録に失敗しました')
    } finally {
      setCreateLoading(false)
    }
  }

  // 編集開始
  const startEdit = (eq: Equipment) => {
    setEditTarget(eq)
    setEditForm({ name: eq.name, category: eq.category, quantity: String(eq.quantity) })
    setEditError(null)
  }

  // 編集保存
  const handleEdit = async (e: FormEvent) => {
    e.preventDefault()
    if (!editTarget) return
    setEditError(null)
    setEditLoading(true)
    try {
      await updateEquipment(editTarget.id, {
        name: editForm.name.trim(),
        category: editForm.category.trim(),
        quantity: Number(editForm.quantity),
      })
      setEditTarget(null)
      await fetchData()
    } catch (err: unknown) {
      const msg = extractErrorMessage(err)
      setEditError(msg ?? '更新に失敗しました')
    } finally {
      setEditLoading(false)
    }
  }

  // 廃棄
  const handleDispose = async (eq: Equipment) => {
    if (!window.confirm(`「${eq.name}」を廃棄しますか？この操作は取り消せません。`)) return
    setError(null)
    try {
      await disposeEquipment(eq.id)
      await fetchData()
    } catch (err: unknown) {
      const msg = extractErrorMessage(err)
      setError(msg ?? '廃棄に失敗しました')
    }
  }

  const totalPages = Math.ceil(total / PAGE_SIZE)

  return (
    <div style={{ padding: '1.5rem', maxWidth: '1100px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0 }}>備品管理</h2>
        <button
          onClick={() => { setShowCreate(true); setCreateForm(emptyForm()); setCreateError(null) }}
          style={btnStyle('#1976d2')}
        >
          ＋ 新規登録
        </button>
      </div>

      {error && <p style={{ color: '#d32f2f', marginBottom: '1rem' }}>{error}</p>}

      {/* 登録モーダル */}
      {showCreate && (
        <Modal title="備品登録" onClose={() => setShowCreate(false)}>
          <form onSubmit={handleCreate}>
            <FormField label="管理番号" required>
              <input
                required
                value={createForm.assetNumber}
                onChange={(e) => setCreateForm({ ...createForm, assetNumber: e.target.value })}
                style={inputStyle}
                placeholder="例: EQ-001"
              />
            </FormField>
            <FormField label="備品名" required>
              <input
                required
                value={createForm.name}
                onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })}
                style={inputStyle}
                placeholder="例: ノートPC"
              />
            </FormField>
            <FormField label="カテゴリ" required>
              <input
                required
                value={createForm.category}
                onChange={(e) => setCreateForm({ ...createForm, category: e.target.value })}
                style={inputStyle}
                placeholder="例: PC"
              />
            </FormField>
            <FormField label="数量" required>
              <input
                required
                type="number"
                min={1}
                value={createForm.quantity}
                onChange={(e) => setCreateForm({ ...createForm, quantity: e.target.value })}
                style={{ ...inputStyle, width: '80px' }}
              />
            </FormField>
            {createError && <p style={{ color: '#d32f2f', fontSize: '0.85rem', margin: '0.5rem 0' }}>{createError}</p>}
            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button type="button" onClick={() => setShowCreate(false)} style={btnStyle('#757575')} disabled={createLoading}>キャンセル</button>
              <button type="submit" style={btnStyle('#1976d2')} disabled={createLoading}>{createLoading ? '登録中...' : '登録'}</button>
            </div>
          </form>
        </Modal>
      )}

      {/* 編集モーダル */}
      {editTarget && (
        <Modal title={`備品編集: ${editTarget.assetNumber}`} onClose={() => setEditTarget(null)}>
          <form onSubmit={handleEdit}>
            <FormField label="備品名" required>
              <input
                required
                value={editForm.name}
                onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                style={inputStyle}
              />
            </FormField>
            <FormField label="カテゴリ" required>
              <input
                required
                value={editForm.category}
                onChange={(e) => setEditForm({ ...editForm, category: e.target.value })}
                style={inputStyle}
              />
            </FormField>
            <FormField label="数量" required>
              <input
                required
                type="number"
                min={1}
                value={editForm.quantity}
                onChange={(e) => setEditForm({ ...editForm, quantity: e.target.value })}
                style={{ ...inputStyle, width: '80px' }}
              />
            </FormField>
            {editError && <p style={{ color: '#d32f2f', fontSize: '0.85rem', margin: '0.5rem 0' }}>{editError}</p>}
            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button type="button" onClick={() => setEditTarget(null)} style={btnStyle('#757575')} disabled={editLoading}>キャンセル</button>
              <button type="submit" style={btnStyle('#1976d2')} disabled={editLoading}>{editLoading ? '保存中...' : '保存'}</button>
            </div>
          </form>
        </Modal>
      )}

      {loading ? (
        <p style={{ color: '#555' }}>読み込み中...</p>
      ) : equipments.length === 0 ? (
        <p style={{ color: '#555', padding: '2rem 0', textAlign: 'center' }}>備品が登録されていません</p>
      ) : (
        <>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: '#f0f0f0' }}>
                {['備品名', '管理番号', 'カテゴリ', '数量', 'ステータス', '操作'].map((h) => (
                  <th key={h} style={{ padding: '0.6rem 0.8rem', textAlign: 'left', borderBottom: '2px solid #ddd', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {equipments.map((eq) => {
                const isDisposed = (eq.status as unknown as string) === 'DISPOSED'
                const isOnLoan = (eq.status as unknown as string) === 'ON_LOAN'
                return (
                  <tr key={eq.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '0.6rem 0.8rem' }}>{eq.name}</td>
                    <td style={{ padding: '0.6rem 0.8rem' }}>{eq.assetNumber}</td>
                    <td style={{ padding: '0.6rem 0.8rem' }}>{eq.category}</td>
                    <td style={{ padding: '0.6rem 0.8rem' }}>{eq.quantity}</td>
                    <td style={{ padding: '0.6rem 0.8rem' }}>
                      <StatusBadge status={eq.status as unknown as string} />
                    </td>
                    <td style={{ padding: '0.6rem 0.8rem', whiteSpace: 'nowrap' }}>
                      <button
                        onClick={() => startEdit(eq)}
                        disabled={isDisposed}
                        style={{ ...btnStyle('#388e3c'), marginRight: '0.4rem', opacity: isDisposed ? 0.4 : 1, cursor: isDisposed ? 'not-allowed' : 'pointer' }}
                      >
                        編集
                      </button>
                      {!isDisposed && (
                        <button
                          onClick={() => handleDispose(eq)}
                          disabled={isOnLoan}
                          title={isOnLoan ? '貸出中のため廃棄できません' : '廃棄する'}
                          style={{ ...btnStyle('#d32f2f'), opacity: isOnLoan ? 0.4 : 1, cursor: isOnLoan ? 'not-allowed' : 'pointer' }}
                        >
                          廃棄
                        </button>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '1rem', justifyContent: 'flex-end' }}>
            <span style={{ fontSize: '0.85rem', color: '#555' }}>
              {total} 件中 {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, total)} 件表示
            </span>
            <button onClick={() => setPage((p) => p - 1)} disabled={page <= 1} style={pageBtn(page <= 1)}>前へ</button>
            <span style={{ fontSize: '0.85rem' }}>{page} / {totalPages}</span>
            <button onClick={() => setPage((p) => p + 1)} disabled={page >= totalPages} style={pageBtn(page >= totalPages)}>次へ</button>
          </div>
        </>
      )}
    </div>
  )
}

// ---- 小コンポーネント ----

function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) {
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div style={{ background: '#fff', borderRadius: '8px', padding: '1.5rem', minWidth: '360px', maxWidth: '480px', width: '100%', boxShadow: '0 4px 24px rgba(0,0,0,0.18)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 600 }}>{title}</h3>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer', color: '#555' }}>✕</button>
        </div>
        {children}
      </div>
    </div>
  )
}

function FormField({ label, required, children }: { label: string; required?: boolean; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: '0.75rem' }}>
      <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem' }}>
        {label}{required && <span style={{ color: '#d32f2f', marginLeft: '2px' }}>*</span>}
      </label>
      {children}
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, { bg: string; color: string }> = {
    AVAILABLE: { bg: '#e8f5e9', color: '#2e7d32' },
    ON_LOAN:   { bg: '#fff3e0', color: '#e65100' },
    DISPOSED:  { bg: '#fafafa', color: '#757575' },
  }
  const s = colors[status] ?? { bg: '#f5f5f5', color: '#333' }
  return (
    <span style={{ padding: '0.2rem 0.6rem', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 500, background: s.bg, color: s.color }}>
      {STATUS_LABEL[status] ?? status}
    </span>
  )
}

// ---- スタイルヘルパー ----

const inputStyle: React.CSSProperties = {
  padding: '0.4rem 0.6rem',
  border: '1px solid #ccc',
  borderRadius: '4px',
  width: '100%',
  boxSizing: 'border-box',
}

const btnStyle = (bg: string): React.CSSProperties => ({
  padding: '0.35rem 0.9rem',
  background: bg,
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '0.85rem',
})

const pageBtn = (disabled: boolean): React.CSSProperties => ({
  padding: '0.3rem 0.8rem',
  border: '1px solid #ccc',
  borderRadius: '4px',
  cursor: disabled ? 'not-allowed' : 'pointer',
  opacity: disabled ? 0.5 : 1,
})

// ---- エラーメッセージ抽出 ----

function extractErrorMessage(err: unknown): string | null {
  if (err && typeof err === 'object') {
    const e = err as { response?: { data?: { message?: string } }; message?: string }
    return e.response?.data?.message ?? e.message ?? null
  }
  return null
}
