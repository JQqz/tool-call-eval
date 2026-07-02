# tool-call-eval

`tool-call-eval` 是一个极简版 Tool Calling 离线评测工具。

它读取两份 JSONL 文件：一份是测试用例，一份是模拟模型输出。然后它会判断模型有没有选对工具、参数有没有传对，并生成一份 Markdown 评测报告。

这个项目不是为了替代成熟评测平台，而是为了把 Tool Calling 评测这件事拆开、做小、做清楚，方便学习和后续扩展。

## 它是做什么的

这个项目回答的是一个很具体的问题：

```text
用户说了一句话，模型有没有调用正确的工具，并传入正确的参数？
```

每条用例会检查：

- 期望工具和实际工具是否一致
- 期望参数是否出现在实际参数里
- 失败原因属于哪一种，比如工具选错、缺少参数、参数值错误、缺少模型输出

## 为什么做它

Tool Calling 在单次演示里可能看起来没问题，但只要用户问法、工具定义、提示词稍微变一下，模型就可能选错工具或漏传参数。

这个项目的价值是：先做一个本地可跑、规则清楚、报告可读的小评测器，用来理解 Tool Calling 评测的基本流程。

适合：

- 刚开始学习 Tool Calling 和 Agent 的人
- 想给自己的 Agent 项目加一个离线回归测试的人
- 想在作品集里展示“我不只是会调 API，也会做评测”的人

## Quick Start

先安装依赖：

```bash
uv sync
```

运行简单示例：

```bash
.venv/bin/python -m tool_call_eval.cli \
  --cases examples/simple/cases.jsonl \
  --outputs examples/simple/model_outputs.jsonl \
  --report reports/simple_report.md
```

这个命令不需要 API key，也不会请求真实 LLM。它只读取本地 JSONL 文件。

你会看到类似输出：

```text
汇总
用例总数：6
工具选择准确率：83.3%
参数匹配准确率：66.7%
报告已写入：reports/simple_report.md
```

## 数据格式

`cases.jsonl` 里每一行是一条标准答案：

```json
{"id":"case_001","input":"帮我算一下 23 * 7","expected_tool":"calculator","expected_args":{"expression":"23 * 7"}}
```

字段含义：

- `id`：用例编号
- `input`：用户输入
- `expected_tool`：期望调用的工具
- `expected_args`：期望传入的参数

`model_outputs.jsonl` 里每一行是一条模拟模型输出：

```json
{"id":"case_001","actual_tool":"calculator","actual_args":{"expression":"23 * 7"}}
```

字段含义：

- `id`：必须和 `cases.jsonl` 里的用例编号对应
- `actual_tool`：模型实际选择的工具
- `actual_args`：模型实际传入的参数

## 报告示例

生成的 Markdown 报告会包含汇总指标、按工具统计、失败原因统计、工具调用对照表和失败用例。

```markdown
## 汇总

| 指标 | 数值 |
|---|---:|
| 用例总数 | 20 |
| 工具选择准确率 | 95.0% |
| 参数匹配准确率 | 85.0% |
```

## DentalBuddy Mock 示例

`examples/dentalbuddy/` 是一个虚构牙科诊所场景数据集，用来模拟更接近真实业务的 Tool Calling 评测。

它覆盖 5 个虚构工具：

- `search_patients`：搜索患者
- `get_patient_detail`：查看患者详情
- `list_appointments`：查询预约
- `list_due_recalls`：查询待回访或复诊提醒
- `search_knowledge`：搜索口腔知识库

运行方式：

```bash
.venv/bin/python -m tool_call_eval.cli \
  --cases examples/dentalbuddy/cases.jsonl \
  --outputs examples/dentalbuddy/model_outputs.jsonl \
  --report reports/dentalbuddy_report.md
```

这份模拟输出里故意放了几条错误，用来展示报告如何识别工具选错、缺少参数和参数值错误。

## 当前限制

`tool-call-eval` v0.1 只做精确匹配。

当前不支持：

- 语义等价判断
- 日期归一化
- 相似表达模糊匹配
- 真实 LLM 调用
- 多轮 Agent trace 评测

另外，`actual_args` 里多出来的字段不会扣分。当前规则只检查 `expected_args` 里要求的字段和值有没有出现在实际输出里。

比如 `this_week` 和明确的起止日期，在 v0.1 里不会被自动认为等价。

## 项目边界

这个项目目前只是一个学习用的小型离线评测器。

它现在做的是：

- 读取本地 JSONL 测试用例
- 读取本地模拟模型输出
- 检查工具名和参数是否匹配
- 生成一份 Markdown 报告

它现在未完成的是：

- 调用真实 LLM
- 连接真实业务系统
- 处理真实数据
- 覆盖生产级评测场景
