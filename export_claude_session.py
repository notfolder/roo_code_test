#!/usr/bin/env python3
"""
Claude セッションエクスポーター
~/.claude/projects/ 配下のセッションを一覧表示し、選択したセッションをMarkdownに出力する
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# 除去するシステムタグのパターン（正規表現）
_SYSTEM_TAG_PATTERN = re.compile(
    r"<(?:ide_opened_file|system-reminder|command-message|command-name|command-args)[^>]*>.*?</(?:ide_opened_file|system-reminder|command-message|command-name|command-args)>",
    re.DOTALL,
)

# ツール出力の最大表示文字数（これを超えたら省略）
TOOL_RESULT_MAX_CHARS = 500


# Claudeのプロジェクトディレクトリ
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"


def parse_jsonl(filepath: Path) -> List[Dict]:
    """JSONLファイルを読み込み、各行をdictのリストとして返す"""
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def get_session_info(jsonl_path: Path) -> Optional[Dict]:
    """
    JSONLファイルからセッションの概要情報を取得する
    Returns: {session_id, project, title, started_at, message_count}
    """
    records = parse_jsonl(jsonl_path)
    if not records:
        return None

    session_id = jsonl_path.stem
    project_dir = jsonl_path.parent.name

    title = None
    started_at = None
    message_count = 0
    project_path = None  # JSONLのcwdフィールドから取得

    for rec in records:
        rec_type = rec.get("type", "")

        # セッションタイトル
        if rec_type == "ai-title" and rec.get("aiTitle"):
            title = rec["aiTitle"]

        # 最初のタイムスタンプ（セッション開始日時）
        if started_at is None and rec.get("timestamp"):
            ts = rec["timestamp"]
            if isinstance(ts, str):
                # ISO形式: "2026-03-28T00:40:12.044Z"
                try:
                    started_at = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    pass
            elif isinstance(ts, (int, float)):
                # エポックミリ秒
                started_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)

        # ユーザー・アシスタントメッセージ数をカウント
        if rec_type in ("user", "assistant"):
            message_count += 1
            # cwdフィールドからプロジェクトパスを取得
            if project_path is None and rec.get("cwd"):
                project_path = rec["cwd"]

    if message_count == 0:
        return None

    # cwdが取得できなかった場合はディレクトリ名をそのまま使用
    if project_path is None:
        project_path = project_dir

    return {
        "session_id": session_id,
        "project_path": project_path,
        "project_dir": project_dir,
        "title": title or "(タイトルなし)",
        "started_at": started_at,
        "message_count": message_count,
        "jsonl_path": jsonl_path,
    }


def collect_all_sessions() -> List[Dict]:
    """全プロジェクトからセッション一覧を収集して返す（新しい順）"""
    if not CLAUDE_PROJECTS_DIR.exists():
        print(f"エラー: {CLAUDE_PROJECTS_DIR} が見つかりません", file=sys.stderr)
        sys.exit(1)

    sessions = []
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl_file in project_dir.glob("*.jsonl"):
            info = get_session_info(jsonl_file)
            if info:
                sessions.append(info)

    # 開始日時の新しい順にソート（日時不明は末尾）
    sessions.sort(
        key=lambda s: s["started_at"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return sessions


def display_session_list(sessions: List[Dict]) -> None:
    """セッション一覧を表示する"""
    print("\n" + "=" * 70)
    print("  Claude セッション一覧")
    print("=" * 70)
    print(f"  {'No':>3}  {'開始日時':<20}  {'プロジェクト / タイトル'}")
    print("-" * 70)

    for i, s in enumerate(sessions, start=1):
        if s["started_at"]:
            # UTC→ローカル時刻に変換して表示
            local_dt = s["started_at"].astimezone()
            date_str = local_dt.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = "不明"

        # プロジェクトパスを短縮表示
        proj = s["project_path"]
        if len(proj) > 30:
            proj = "..." + proj[-27:]

        title = s["title"]
        if len(title) > 40:
            title = title[:37] + "..."

        print(f"  {i:>3}  {date_str:<20}  [{proj}]")
        print(f"       {'':20}  {title}  ({s['message_count']}件)")
        print()

    print("=" * 70)


def _clean_text(text: str) -> str:
    """システムタグを除去してテキストを返す"""
    return _SYSTEM_TAG_PATTERN.sub("", text).strip()


def _truncate(text: str, max_chars: int = TOOL_RESULT_MAX_CHARS) -> str:
    """長すぎるテキストを省略表示する"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n*...省略（全 {len(text):,} 文字中 {max_chars:,} 文字を表示）*"


def _build_tool_results_map(records: List[Dict]) -> Dict[str, str]:
    """
    全レコードを走査して tool_use_id → ツール出力テキスト のマップを構築する
    ツール結果は user ロールの tool_result アイテムとして格納される
    """
    results: Dict[str, str] = {}
    for rec in records:
        message = rec.get("message", {})
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict) or item.get("type") != "tool_result":
                continue
            tool_use_id = item.get("tool_use_id", "")
            rc = item.get("content", "")
            if isinstance(rc, list):
                text = "\n".join(r.get("text", "") for r in rc if isinstance(r, dict))
            else:
                text = str(rc)
            # system-reminder タグを除去
            text = _clean_text(text)
            results[tool_use_id] = text
    return results


def _extract_user_text(content) -> str:
    """
    ユーザーメッセージから人間が入力したテキストのみを抽出する
    tool_result（ツール応答）は人間の発言ではないためスキップする
    """
    if isinstance(content, str):
        return _clean_text(content)

    if not isinstance(content, list):
        return _clean_text(str(content))

    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(_clean_text(item.get("text", "")))
        elif isinstance(item, str):
            parts.append(_clean_text(item))
        # tool_result はスキップ（ツールの応答は人間の発言ではない）

    return "\n".join(p for p in parts if p)


def _extract_assistant_content(content, tool_results: Dict[str, str]) -> str:
    """
    アシスタントメッセージのコンテンツを整形する
    text はそのまま、tool_use はツール呼び出しと対応する結果をセットで表示する
    thinking はスキップする
    """
    if isinstance(content, str):
        return _clean_text(content)

    if not isinstance(content, list):
        return _clean_text(str(content))

    parts = []
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type", "")

        if item_type == "text":
            parts.append(_clean_text(item.get("text", "")))

        elif item_type == "tool_use":
            # ツール呼び出しの表示
            tool_name = item.get("name", "tool")
            tool_id = item.get("id", "")
            tool_input = item.get("input", {})

            # 入力パラメータ（大きすぎる場合は省略）
            input_str = json.dumps(tool_input, ensure_ascii=False, indent=2)
            input_str = _truncate(input_str, TOOL_RESULT_MAX_CHARS)

            block = [f"> **🔧 ツール呼び出し: `{tool_name}`**"]
            block.append(f"> ```json\n> {input_str.replace(chr(10), chr(10) + '> ')}\n> ```")

            # 対応するツール出力があれば表示
            if tool_id in tool_results:
                result_text = _truncate(tool_results[tool_id], TOOL_RESULT_MAX_CHARS)
                result_lines = result_text.replace("\r\n", "\n").replace("\r", "\n")
                block.append(f"> **結果:**")
                block.append(f"> ```\n> {result_lines.replace(chr(10), chr(10) + '> ')}\n> ```")

            parts.append("\n".join(block))

        # thinking はスキップ

    return "\n\n".join(p for p in parts if p)


def _parse_timestamp(rec: Dict) -> str:
    """レコードのタイムスタンプを HH:MM:SS 文字列に変換する"""
    ts = rec.get("timestamp")
    if not ts:
        return ""
    try:
        if isinstance(ts, str):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
        else:
            dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone()
        return f" _{dt.strftime('%H:%M:%S')}_"
    except Exception:
        return ""


def build_markdown(session_info: Dict) -> str:
    """
    セッションのJSONLを読み込み、Markdown文字列を生成する
    - ユーザーメッセージ: 人間が入力したテキストのみ（tool_result はスキップ）
    - アシスタントメッセージ: テキスト + ツール呼び出し（結果付き・省略あり）
    """
    records = parse_jsonl(session_info["jsonl_path"])

    # 全レコードから tool_use_id → 結果 のマップを先に構築
    tool_results = _build_tool_results_map(records)

    lines = []

    # ヘッダー
    lines.append(f"# {session_info['title']}")
    lines.append("")
    lines.append(f"- **セッションID**: `{session_info['session_id']}`")
    lines.append(f"- **プロジェクト**: `{session_info['project_path']}`")
    if session_info["started_at"]:
        local_dt = session_info["started_at"].astimezone()
        lines.append(f"- **開始日時**: {local_dt.strftime('%Y年%m月%d日 %H:%M:%S')}")
    lines.append(f"- **メッセージ数**: {session_info['message_count']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ユーザー・アシスタントのメッセージを順番に出力
    for rec in records:
        rec_type = rec.get("type", "")
        if rec_type not in ("user", "assistant"):
            continue

        message = rec.get("message", {})
        role = message.get("role", rec_type)
        content = message.get("content", "")
        ts_str = _parse_timestamp(rec)

        if role == "user":
            # 人間が入力したテキストのみ抽出（tool_result は除外）
            text = _extract_user_text(content)
            if not text.strip():
                # tool_result のみのメッセージはスキップ（人間の発言ではない）
                continue
            lines.append(f"## 👤 ユーザー{ts_str}")
            lines.append("")
            lines.append(text.strip())

        else:
            # アシスタント: テキスト + ツール呼び出し（thinking はスキップ）
            # thinking のみのメッセージをスキップ
            if isinstance(content, list):
                has_visible = any(
                    c.get("type") in ("text", "tool_use")
                    for c in content
                    if isinstance(c, dict)
                )
                if not has_visible:
                    continue

            text = _extract_assistant_content(content, tool_results)
            if not text.strip():
                continue

            model = message.get("model", "")
            model_note = f" `{model}`" if model else ""
            lines.append(f"## 🤖 アシスタント{model_note}{ts_str}")
            lines.append("")
            lines.append(text.strip())

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def select_session(sessions: List[Dict]) -> Optional[Dict]:
    """ユーザーにセッション番号を入力させて選択されたセッションを返す"""
    while True:
        try:
            raw = input("エクスポートするセッション番号を入力してください (q で終了): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if raw.lower() in ("q", "quit", "exit"):
            return None

        try:
            num = int(raw)
            if 1 <= num <= len(sessions):
                return sessions[num - 1]
            else:
                print(f"  1〜{len(sessions)} の番号を入力してください")
        except ValueError:
            print("  数値を入力してください")


def choose_output_path(session_info: dict) -> Path:
    """出力ファイルパスをユーザーに確認する"""
    # デフォルトのファイル名
    title_slug = session_info["title"][:40]
    # ファイル名に使えない文字を置換
    for ch in r'\/:*?"<>|':
        title_slug = title_slug.replace(ch, "_")
    title_slug = title_slug.strip().replace(" ", "_")

    default_name = f"claude_session_{title_slug}.md"
    default_path = Path.cwd() / default_name

    print(f"\nデフォルト出力先: {default_path}")
    raw = input("出力ファイルパスを入力 (Enter でデフォルト): ").strip()

    if raw:
        out_path = Path(raw).expanduser()
    else:
        out_path = default_path

    return out_path


def main():
    print("Claudeセッションを読み込み中...")
    sessions = collect_all_sessions()

    if not sessions:
        print("セッションが見つかりませんでした。")
        sys.exit(0)

    display_session_list(sessions)

    # セッション選択
    selected = select_session(sessions)
    if selected is None:
        print("終了します。")
        sys.exit(0)

    print(f"\n選択: [{selected['project_path']}] {selected['title']}")

    # 出力先決定
    out_path = choose_output_path(selected)

    # Markdown生成
    print("\nMarkdownを生成中...")
    markdown_text = build_markdown(selected)

    # ファイル書き込み
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown_text, encoding="utf-8")

    print(f"\n✅ エクスポート完了: {out_path}")
    print(f"   文字数: {len(markdown_text):,} 文字")


if __name__ == "__main__":
    main()
