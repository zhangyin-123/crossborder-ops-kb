# 跨境电商运营知识库

[知识索引](knowledge/INDEX.md) · [共同规则](AGENTS.md) · [官方来源](sources/official.md) · [待审核分支](https://github.com/zhangyin-123/crossborder-ops-kb/tree/review/intake)

第一期使用一个 GitHub 私有仓库和一台 Mac。Codex 与 Muse Code 通过同一个本地 MCP 服务读取卡片。两个客户端都使用这台 Mac 上的同一份工作目录，新增草稿可在下一次查询时看到。GitHub 保存版本和审核记录。

## 查资料

向任一 Agent 说「在跨境知识库查马来西亚补货，只引用已审核资料」。检索工具为 `search_knowledge`，按返回的 ID 调用 `read_knowledge` 获取正文和出处。搜索支持中文和英文，多词用空格分隔。结果包含来源、市场、核对日期以及已知的生效和失效日期。

初次使用先看草稿，例如「查询草稿中的 SKU 补货，列出来源和核对日」。对客户答复使用默认的 approved 范围，仅采纳主线已合并且在有效期内的卡片。没有结果时，说明「知识库暂无经审核依据」。

终端也可以执行：

```sh
python3 scripts/search_kb.py "库存 SKU" --status draft
python3 scripts/search_kb.py "补货" --json
```

## 加资料与审核

1. 在这台 Mac 的 `review/intake` 分支中，将已获授权、已脱敏的 Markdown 摘要放进 `inbox/`。每篇写清一级标题、地区和原始来源链接。原始收件不进入 Git。
2. 运行 `python3 scripts/organize_kb.py` 和 `python3 scripts/validate_kb.py`。整理器按平台和主题生成草稿、刷新索引。同一份原件可以重复导入。缺标题、主题或来源的资料归到 `needs-review`。修改已有草稿时直接改卡片，再运行 `organize_kb.py --index-only`。
3. 检查本次变更，只将准许共享的摘要和索引提交到审核分支。默认使用同一个待审分支，两个 Agent 和审核人可查阅同一批资料。
4. 人工审核来源、适用地区、卖家类型、政策日期和版权；通过后在审核分支将对应卡片的 `status` 改为 `approved`，重新生成索引并校验，使用拉取请求合并到 `main`。审核人可以只批准部分卡片。仍为 draft 的卡片即使合并也不会作为正式答案。
5. 其他设备合并后，这台 Mac 运行 `git fetch origin` 即可让两端查询到最新正式资料。日更任务也执行此步骤。草稿检索读取本地工作目录，正式检索优先读取最近获取的 `origin/main`。断网期间，本机可以查询上次已同步的正式资料。

最小收件示例：

```markdown
# TikTok Shop 马来西亚｜按 SKU 排查缺货
来源：https://seller-my.tiktok.com/……具体官方文章……
写下自己核对过的操作要点、适用范围和例外。
```

## 每日维护

Codex 本地任务每天北京时间 09:00 扫描[官方来源](sources/official.md)，检查是否有新增或实质修订。发现新内容时生成草稿并推送审核分支；无更新时记录检查结果。任务使用本机登录和网络，Mac 关机或运行环境不可用会影响准点执行。第一期无需租服务器。

## 在另一台 Mac 恢复检索

克隆本私库，检出审核分支，然后运行：

```sh
uv sync --locked --python 3.12
codex mcp add crossborder-ops-kb -- "$PWD/.venv/bin/python" "$PWD/scripts/mcp_server.py"
```

Muse Code 的 MCP 设置使用 `stdio` 传输，服务名同为 `crossborder-ops-kb`。将 command 指向上述 Python 的绝对路径，以脚本的绝对路径作为唯一参数。在 Muse Code 中运行 `/mcp` 查看连接和工具。克隆库之后，GitHub 登录以及本机定时任务应在新设备上单独配置。
