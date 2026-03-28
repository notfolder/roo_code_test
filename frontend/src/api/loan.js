/**
 * 貸出API
 * 貸出記録の一覧取得・貸出登録・返却登録のAPIリクエストを提供する
 */
import apiClient from './client'

const loanApi = {
  /** 貸出記録一覧を取得する */
  getAll() {
    return apiClient.get('/api/loans/')
  },

  /** 貸出を登録する */
  create(equipmentId, borrowerAccountId) {
    return apiClient.post('/api/loans/', {
      equipment_id: equipmentId,
      borrower_account_id: borrowerAccountId,
    })
  },

  /** 返却を登録する */
  returnLoan(loanId) {
    return apiClient.put(`/api/loans/${loanId}/return`)
  },
}

export default loanApi
