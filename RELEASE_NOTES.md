# 发布说明

## v0.1.0

`agent-tool-lab` v0.1.0 是第一个离线评测版本，用来学习和演示 LLM Tool Calling 的基础评测流程。

### 这个版本支持

- 读取 `cases.jsonl` 测试用例
- 读取 `model_outputs.jsonl` 模拟模型输出
- 计算工具选择准确率
- 计算参数精确匹配准确率
- 识别常见失败原因：
  - 工具选择错误
  - 缺少参数
  - 参数值错误
  - 缺少模型输出
- 生成 Markdown 评测报告，包含：
  - 汇总指标
  - 按工具统计
  - 失败原因统计
  - 工具调用对照表
  - 失败用例列表
- 不需要 API key 就能运行 simple 和 DentalBuddy Mock 两组示例

### 运行示例

安装依赖：

```bash
uv sync
```

运行 simple 示例：

```bash
.venv/bin/python -m agent_tool_lab.cli \
  --cases examples/simple/cases.jsonl \
  --outputs examples/simple/model_outputs.jsonl \
  --report reports/simple_report.md
```

运行 DentalBuddy Mock 示例：

```bash
.venv/bin/python -m agent_tool_lab.cli \
  --cases examples/dentalbuddy/cases.jsonl \
  --outputs examples/dentalbuddy/model_outputs.jsonl \
  --report reports/dentalbuddy_report.md
```

运行测试：

```bash
uv run pytest
```

### 已知限制

- 不调用真实 LLM
- 不做语义等价判断
- 不做日期归一化
- 不支持工具名或参数别名映射
- 不支持多轮 Agent trace 评测
- 不生成 HTML 报告
