# roo_code_test
roo codeで仕様書から詳細設計、コードを生成するテスト

## Playwright MCP サーバー設定

Docker Composeの`test_playwright`サービス（port 9999）をMCPサーバーとして各ツールに接続する方法。

起動コマンド:
```bash
docker compose up test_playwright
```

エンドポイント: `http://localhost:9999/mcp`

### GitHub Copilot

`.vscode/mcp.json` に追加:

```json
{
  "servers": {
    "test_playwright": {
      "type": "http",
      "url": "http://localhost:9999/mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http test_playwright http://localhost:9999/mcp
```

### Roo Code

`settings.json` に追加:

```json
{
  "roo-cline.mcpServers": {
    "test_playwright": {
      "disabled": false,
      "timeout": 60,
      "type": "streamable-http",
      "url": "http://localhost:9999/mcp"
    }
  }
}
```

> **注意**: Playwright MCP v0.0.70以降、`--port`で起動した場合のエンドポイントは `/mcp` です（`/sse` ではありません）。
