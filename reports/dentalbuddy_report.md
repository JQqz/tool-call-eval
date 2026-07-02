# 工具调用评测报告

## 汇总

| 指标 | 数值 |
|---|---:|
| 用例总数 | 20 |
| 工具选择准确率 | 95.0% |
| 参数匹配准确率 | 85.0% |

## 按工具统计

| 期望工具 | 用例数 | 工具选择准确率 | 参数匹配准确率 |
|---|---:|---:|---:|
| get_patient_detail | 3 | 100.0% | 66.7% |
| list_appointments | 4 | 75.0% | 75.0% |
| list_due_recalls | 3 | 100.0% | 100.0% |
| search_knowledge | 5 | 100.0% | 80.0% |
| search_patients | 5 | 100.0% | 100.0% |

## 失败原因统计

| 失败原因 | 次数 |
|---|---:|
| 缺少参数 | 1 |
| 参数值错误 | 2 |
| 工具选择错误 | 1 |

## 工具调用对照表

| 期望调用 \ 实际调用 | get_patient_detail | list_appointments | list_due_recalls | search_knowledge | search_patients |
|---|---:|---:|---:|---:|---:|
| get_patient_detail | 3 | 0 | 0 | 0 | 0 |
| list_appointments | 0 | 3 | 0 | 0 | 1 |
| list_due_recalls | 0 | 0 | 3 | 0 | 0 |
| search_knowledge | 0 | 0 | 0 | 5 | 0 |
| search_patients | 0 | 0 | 0 | 0 | 5 |

## 失败用例

| 用例 ID | 用户输入 | 期望工具 | 实际工具 | 失败原因 |
|---|---|---|---|---|
| dental_007 | 看一下电话尾号 3821 那位患者的详细资料 | get_patient_detail | get_patient_detail | 缺少参数 |
| dental_009 | 今天有哪些预约？ | list_appointments | search_patients | 工具选择错误 |
| dental_011 | 下周一上午有没有预约？ | list_appointments | list_appointments | 参数值错误 |
| dental_020 | 种植牙术后应该注意什么？ | search_knowledge | search_knowledge | 参数值错误 |
