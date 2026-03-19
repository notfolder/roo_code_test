import { Link } from "react-router-dom";
import "./layout.css";

// シンプルなレイアウトとナビゲーション
export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="layout">
      <header className="layout__header">
        <div className="layout__title">備品管理・貸出予約</div>
        <nav className="layout__nav">
          <Link to="/equipment">備品一覧</Link>
          <Link to="/availability">空き状況</Link>
          <Link to="/reservations">予約</Link>
          <Link to="/login">ログイン</Link>
        </nav>
      </header>
      <main className="layout__main">{children}</main>
    </div>
  );
}
