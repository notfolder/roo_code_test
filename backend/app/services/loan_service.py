"""
貸出サービス
貸出・返却の業務ロジックとトランザクション制御を担う
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.equipment_repository import EquipmentRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.account_repository import AccountRepository
from app.schemas.loan import LoanCreate, LoanResponse


class LoanService:
    """貸出・返却業務ロジックを提供するサービス"""

    @staticmethod
    def list_loans(db: Session) -> list[LoanResponse]:
        """
        全貸出記録の一覧を返す
        """
        loans = LoanRepository.find_all(db)
        return [LoanService._to_response(loan) for loan in loans]

    @staticmethod
    def create_loan(db: Session, data: LoanCreate, operator_id: int) -> LoanResponse:
        """
        貸出を登録する（トランザクション制御あり）
        1. 備品を悲観的ロック（FOR UPDATE）で取得する
        2. 貸出可能状態（available）であることを確認する
        3. 備品状態を貸出中（borrowed）に更新する
        4. 貸出記録を登録する
        二重貸出防止のため、備品の状態確認から更新をトランザクション内で実行する
        """
        # 借りる社員のアカウントが存在することを確認する
        borrower = AccountRepository.find_by_id(db, data.borrower_account_id)
        if borrower is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された社員が見つかりません",
            )

        # 悲観的ロック付きで備品を取得し、状態を確認する
        equipment = EquipmentRepository.find_by_id_for_update(db, data.equipment_id)
        if equipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された備品が見つかりません",
            )
        if equipment.status != "available":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="この備品は既に貸出中です",
            )

        # 備品状態を貸出中に更新し、貸出記録を登録する
        EquipmentRepository.update_status(db, equipment, "borrowed")
        loan = LoanRepository.create(db, data, operator_id)
        db.commit()
        return LoanService._to_response(loan)

    @staticmethod
    def return_loan(db: Session, loan_id: int, operator_id: int) -> LoanResponse:
        """
        返却を登録する（トランザクション制御あり）
        1. 対象の貸出記録（未返却）を取得する
        2. 備品状態を貸出可能（available）に更新する
        3. 貸出記録に返却日時を設定する
        """
        # 貸出記録を取得する（未返却のもの）
        loan = LoanRepository.find_by_id(db, loan_id)
        if loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された貸出記録が見つかりません",
            )
        if loan.returned_at is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="この貸出記録は既に返却済みです",
            )

        # 備品状態を貸出可能に戻し、返却日時を記録する
        EquipmentRepository.update_status(db, loan.equipment, "available")
        updated_loan = LoanRepository.set_returned(db, loan)
        db.commit()
        # コミット後にリレーションを再ロードする
        db.refresh(updated_loan)
        return LoanService._to_response(updated_loan)

    @staticmethod
    def _to_response(loan) -> LoanResponse:
        """
        LoanRecordオブジェクトをLoanResponseスキーマに変換する共通処理
        """
        return LoanResponse(
            id=loan.id,
            equipment_id=loan.equipment_id,
            management_number=loan.equipment.management_number,
            equipment_name=loan.equipment.name,
            borrower_name=loan.borrower.account_name,
            operator_name=loan.operator.account_name,
            loaned_at=loan.loaned_at,
            returned_at=loan.returned_at,
        )
