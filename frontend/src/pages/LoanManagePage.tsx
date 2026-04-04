import { useState, useEffect, useCallback, FormEvent } from 'react'
import type { Equipment, LoanRecord } from '../types'
import { getEquipments } from '../api/equipmentApi'
import { createLoan, returnLoan, getLoansByUser } from '../api/loanApi'

const today = () => new Date().toISOString().slice(0, 10)

interface LoanForm {
  equipmentId: string
  userId: string
  loanDate: string
  dueDate: string
}

const emptyForm = (): LoanForm => ({
  equipmentId: '',
  userId: '',
  loanDate: today(),
  dueDate: '',
})

export default function LoanManagePage() {
  const [availableEquipments, setAvailableEquipments] = useState<Equipment[]>([])
  const [equipmentsLoading, setEquipmentsLoading] = useState(false)

  // 貸出登録フォーム
  const [form, setForm] = useState<LoanForm>(emptyForm())
  const [formError, setFormError] = useState<string | null>(null)
  const [formLoading, setFormLoading] = useState(false)
  const [formSuccess, setFormSuccess] = useState<string | null>(null)

  // ユーザー検索
  const [searchUserId, setSearchUserId] = useState('')
  const [loans, setLoans] = useState<LoanRecord[]>([])
  const [searchLoading, setSearchLoading] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)
  const [returnError, setReturnError] = useState<string | null>(null)

  const fetchAvailableEquipments = useCallback(async () => {
    setEquipmentsLoading(true)
    try {
      const result = await getEquipments(1, 200)
      setAvailableEquipments(result.data.filter((eq) => (eq.status as unknown as string) === 'AVAILABLE'))
    } catch {
      // 取得失敗時は空のまま
    } finally {
      setEquipmentsLoading(false)
    }
  }, [])

  useEffect(() => { fetchAvailableEquipments() }, [fetchAvailableEquipments])

  const handleCreateLoan = async (e: FormEvent) => {
    e.preventDefault()
    setFormError(null)
    setFormSuccess(null)
    setFormLoading(true)
    try {
      await createLoan(form)
      setFormSuccess('貸出登録が完了しました')
      setForm(emptyForm())
      await fetchAvailableEquipments()
      // 検索中のユーザーがいれば再取得
      if (searchUserId) await fetchLoansByUser(searchUserId)
    } catch (err: unknown) {
      setFormError(extractErrorMessage(err) ?? '貸出登録に失敗しました')
    } finally {
      setFormLoading(false)
    }
  }

  const fetchLoansByUser = async (userId: string) => {
    setSearchLoading(true)
    setSearchError(null)
    setReturnError(null)
    try {
      const result = await getLoansByUser(userId)
      setLoans(result)
    } catch (err: unknown) {
      setSearchError(extractErrorMessage(err) ?? '貸出履歴の取得に失敗しました')
      setLoans([])
    } finally {
      setSearchLoading(false)
    }
  }

  const handleSearch = (e: FormEvent) => {
    e.preventDefault()
    if (!searchUserId.trim()) return
    fetchLoansByUser(searchUserId.trim())
  }

  const handleReturn = async (loan: LoanRecord) => {
    if (!window.confirm('この貸出を返却済みにしますか？')) return
    setReturnError(null)
    try {
      await returnLoan(loan.id)
      await fetchLoansByUser(searchUserId)
      await fetchAvailableEquipments()
    } catch (err: unknown) {
      setReturnError(extractErrorMessage(err) ?? '返却登録に失敗しました')
    }
  }

  const activeLoans = loans.filter((l) => !l.returnedAt)
  const returnedLoans = loans.filter((l) => l.returnedAt)

  return (
    <div style={{ padding: '1.5rem', maxWidth: '900px', margin: '0 auto' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1.5rem' }}>貸出・返却管理</h2>

      {/* 貸出登録フォーム */}
      <section style={sectionStyle}>
        <h3 style={sectionTitle}>貸出登録</h3>
        <form onSubmit={handleCreateLoan}>
          <FormField label="備品" required>
            <select
              required
              value={form.equipmentId}
              onChange={(e) => setForm({ ...form, equipmentId: e.target.value })}
              style={inputStyle}
              disabled={equipmentsLoading}
            >
              <option value="">-- 備品を選択 --</option>
              {availableEquipments.map((eq) => (
                <option key={eq.id} value={eq.id}>
                  {eq.name}（{eq.assetNumber}）
                </option>
              ))}
            </select>
            {availableEquipments.length === 0 && !equipmentsLoading && (
              <p style={{ fontSize: '0.8rem', color: '#888', margin: '0.25rem 0 0' }}>利用可能な備品がありません</p>
            )}
          </FormField>

          <FormField label="貸出先ユーザー ID" required>
            <input
              required
              type="text"
              value={form.userId}
              onChange={(e) => setForm({ ...form, userId: e.target.value })}
              style={inputStyle}
              placeholder="例: user-uuid-xxxx"
            />
          </FormField>

          <div style={{ display: 'flex', gap: '1rem' }}>
            <FormField label="貸出日" required>
              <input
                required
                type="date"
                value={form.loanDate}
                onChange={(e) => setForm({ ...form, loanDate: e.target.value })}
                style={{ ...inputStyle, width: 'auto' }}
              />
            </FormField>
            <FormField label="返却予定日" required>
              <input
                required
                type="date"
                value={form.dueDate}
                min={form.loanDate}
                onChange={(e) => setForm({ ...form, dueDate: e.target.value })}
                style={{ ...inputStyle, width: 'auto' }}
              />
            </FormField>
          </div>

          {formError && <p style={errorStyle}>{formError}</p>}
          {formSuccess && <p style={{ color: '#2e7d32', fontSize: '0.9rem', margin: '0.5rem 0' }}>{formSuccess}</p>}

          <button type="submit" style={btnStyle('#1976d2')} disabled={formLoading}>
            {formLoading ? '登録中...' : '貸出登録'}
          </button>
        </form>
      </section>

      {/* 貸出履歴検索 */}
      <section style={sectionStyle}>
        <h3 style={sectionTitle}>貸出履歴検索（ユーザー ID）</h3>
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
          <input
            type="text"
            value={searchUserId}
            onChange={(e) => setSearchUserId(e.target.value)}
            placeholder="ユーザー ID を入力"
            style={{ ...inputStyle, flex: 1 }}
          />
          <button type="submit" style={btnStyle('#555')} disabled={searchLoading || !searchUserId.trim()}>
            {searchLoading ? '検索中...' : '検索'}
          </button>
        </form>

        {searchError && <p style={errorStyle}>{searchError}</p>}
        {returnError && <p style={errorStyle}>{returnError}</p>}

        {loans.length > 0 && (
          <>
            {activeLoans.length > 0 && (
              <>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 600, margin: '0 0 0.5rem' }}>未返却（{activeLoans.length} 件）</h4>
                <LoanTable loans={activeLoans} onReturn={handleReturn} showReturn />
              </>
            )}
            {returnedLoans.length > 0 && (
              <>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 600, margin: '1rem 0 0.5rem' }}>返却済み（{returnedLoans.length} 件）</h4>
                <LoanTable loans={returnedLoans} onReturn={handleReturn} showReturn={false} />
              </>
            )}
          </>
        )}

        {!searchLoading && loans.length === 0 && searchUserId && !searchError && (
          <p style={{ color: '#888', fontSize: '0.9rem' }}>貸出履歴がありません</p>
        )}
      </section>
    </div>
  )
}

// ---- サブコンポーネント ----

function LoanTable({
  loans,
  onReturn,
  showReturn,
}: {
  loans: LoanRecord[]
  onReturn: (loan: LoanRecord) => void
  showReturn: boolean
}) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem', marginBottom: '0.5rem' }}>
      <thead>
        <tr style={{ background: '#f5f5f5' }}>
          {['備品 ID', '貸出日', '返却予定日', '返却日', ...(showReturn ? ['操作'] : [])].map((h) => (
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
            {showReturn && (
              <td style={tdStyle}>
                <button onClick={() => onReturn(loan)} style={btnStyle('#e65100')}>
                  返却登録
                </button>
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
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
