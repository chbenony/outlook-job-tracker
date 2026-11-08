You are reviewing a pull request. Run `git diff HEAD^1 HEAD` to see the PR's changes, where `HEAD` is the
merge commit and `HEAD^1` is the base branch. Look at the surrounding code context and provide feedback.

This project is a Python MCP server that reads one Outlook mail folder through Microsoft Graph, so that
an AI assistant can track job applications. It uses `mcp` (2.x, `MCPServer`), `msal`, and `httpx`.

Focus on:

- Correctness: logic errors, edge cases, unhandled error responses from msal or Graph
- Async: blocking calls inside `async` functions, unawaited coroutines, concurrency bugs
- Security: tokens, refresh tokens, or `.env` values being logged, printed, or committed; requests that
  reach beyond the configured job folder or ask for more than the `Mail.Read` scope
- MCP: anything written to stdout inside the MCP server (it corrupts the stdio protocol); tool
  docstrings that would mislead the assistant calling the tool
- Clarity: confusing naming, missing context that would help a reviewer

Do not comment on:

- Formatting or style that a linter would catch (ruff runs separately)
- Personal preference where the existing code is already reasonable

Only flag API or library misuse if you can cite the documentation or source that shows it.

Keep the review concise. If the change looks good, say so briefly instead of inventing nitpicks.

Report each issue as a separate entry in `comments`, anchored to the specific file and line it applies to (use the line number in the new/right-hand version of the file, and only lines that are actually part of the diff). Each comment body should explain the concrete problem and suggest a fix. Use `summary` for a short overall verdict (1-3 sentences) — do not repeat the per-line issues there. If there are no issues, return an empty `comments` array and say so in `summary`.
