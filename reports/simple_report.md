# 工具调用评测报告

## 汇总

| 指标 | 数值 |
|---|---:|
| 用例总数 | 6 |
| 工具选择准确率 | 83.3% |
| 参数匹配准确率 | 66.7% |

## 按工具统计

| 期望工具 | 用例数 | 工具选择准确率 | 参数匹配准确率 |
|---|---:|---:|---:|
| calculator | 1 | 100.0% | 100.0% |
| search_appointments | 3 | 66.7% | 66.7% |
| search_knowledge_base | 2 | 100.0% | 50.0% |

## 失败原因统计

| 失败原因 | 次数 |
|---|---:|
| 缺少参数 | 1 |
| 参数值错误 | 1 |
| 工具选择错误 | 1 |

## 工具调用对照表

| 期望调用 \ 实际调用 | calculator | search_appointments | search_knowledge_base |
|---|---:|---:|---:|
| calculator | 1 | 0 | 0 |
| search_appointments | 0 | 2 | 1 |
| search_knowledge_base | 0 | 0 | 2 |

## 失败用例

| 用例 ID | 用户输入 | 期望工具 | 实际工具 | 失败原因 |
|---|---|---|---|---|
| case_004 | 帮我查一下患者李雷的预约 | search_appointments | search_knowledge_base | 工具选择错误 |
| case_005 | 帮我查一下患者赵敏的预约 | search_appointments | search_appointments | 缺少参数 |
| case_006 | 帮我搜索一下拔牙后的饮食注意事项 | search_knowledge_base | search_knowledge_base | 参数值错误 |
