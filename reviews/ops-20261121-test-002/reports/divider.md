# 可裁剪抽屉分隔件（4条装） · 单品模拟连通报告

任务 `OPS-20261121-TEST-002` · SKU `TEST-MY-002-DIVIDER` · MY / SIM-MY-002 · MYR。本品六环记录 6 条，节点回执 3 份，主批分发结果为 VERIFIED。 [总报告](../report.md)

## 1　选品与日常款测算

家居收纳。合成产品含包装 260 g，单件上限 2,500 g。模拟成本来源为本单夹具，到仓 CNY 8.00；按模型计入物流和其他单件成本后为 MYR 13.24。真实货源、毛利、实物尺寸及材质、商标及销售辖区证据均待核实。

| 含税面价 MYR | 商家 8% 券后实付 MYR | 扣税净收入 MYR | 毛利率 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 29.90 | 27.51 | 25.01 | 47.04% | 4.39 |

毛利率分母是扣税净收入，精确百分数为 13263200/281957。按未舍入值检查 8% 日常门槛。三种日常场景与费项明细见 STEP01。[流程日志](../flow.jsonl)

## 2　市场与竞品分析

模拟马来语搜索词 **sekat laci boleh potong**。统计窗为 2026-10-24 至 2026-11-20（28天），虚构搜索 48 次、商品点击 12 次。每款一个模拟对照，未观测市场销量或买家评论。

本地模拟对照 SIM-MY-COMP-DIVIDER 为模拟固定格抽屉托盘，售价 MYR 22.00。其特征为六个固定格，格宽无法调整。

预设使用场景为在抽屉内分隔餐具或零碎配件，适配分区布局。买前问题为“小抽屉能否裁短分隔条，分隔条如何交叉固定？”

## 3　素材规划、示意图与权利记录

本 SKU 的展示计划为“示意图展示分隔条的插槽与交叉连接，文案明确条长与条数。”
本地按商品几何轮廓绘制 320 × 240 SVG，版本 v1。图内没有照片、外部图像、字体或音轨。

![可裁剪抽屉分隔件（4条装）的合成结构示意图](../assets/test-my-002-divider.svg)

测试许可 `SIM-LIC-TEST-MY-002-DIVIDER`，范围 `simulated-commercial-review-only`，地区 MY，有效期 2026-11-01 至 2026-12-31。核验图像 SHA-256 为 `494454d0445bf82e29011b4c7d93319919f2061701b0655a76df867ef5d5cd0f`。 [许可登记](../assets/test-my-002-divider.licence.json)

## 4　英文标题与五点

**Trim-to-Fit Slotted Drawer Dividers, Set of Four**

1. Four ivory divider strips for arranging a drawer into sections.
2. Each strip measures 30 cm long and 5 cm high before trimming.
3. Line up the slots and press two strips together to form a cross.
4. Measure the drawer interior before cutting the strips to length.
5. Arrange the sections around cutlery, stationery or small accessories.

模拟稿版本 v1，文本 SHA-256 为 `6921c0c3f25670fda376cfcca4b548107388f155164d25136434cb1d5872acc5`。实店文案待补适用规则及实物依据。

## 5　四项合规核验

R10 图片测试许可通过。R05 在马来站为不适用，核查 UK 在售 SKU 0 个，更新 UK 全量基线为否。P0 主批冻结为否。本次门禁仅放行测试包。

R03 的模拟秒杀价为 MYR 25.42，每人限购 1，活动配额 3。两种情景均纳入同一时点前台快照的自动券。

| 情景 | 券后买家付款 MYR | 毛利率 | 专用底线 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 误叠商家 8% 券 | 22.39 | 34.92% | 13.00% | 1.01 |
| 排除商家 8% 券 | 24.42 | 40.34% | 13.00% | 2.35 |

R03 主批核验通过，活动提交为否。在分离的故障试验中，对本 SKU 的投递尝试被拒 4 次。[风险探针日志](../risk-probes.jsonl)

## 6　三节点签收与回读

同一请求 `SIM-002-MY-94adb6a537-TEST-MY-002-DIVIDER-ROUTE`。WorkBuddy 核对 750 字节图片正文、5 条英文要点及原稿版本。妙手返回模拟店号 `SIM-MIAO-MY-002`、采集箱对象 `SIM-BOX-002-01`，对象状态 SIMULATED_UNPUBLISHED，本次商品草稿号未生成。紫鸟模拟环境为 `SIM-ZN-MY-002`，入场检查 9/9 项通过。

| 节点 | 回执 ID | 接收进程 PID | 回执时间 |
| --- | --- | --- | --- |
| MiaoshouERP | `SIM-002-MY-94adb6a537-TEST-MY-002-DIVIDER-ROUTE/MiaoshouERP` | 80948 | 2026-11-20T17:24:34.710247+00:00 |
| WorkBuddy | `SIM-002-MY-94adb6a537-TEST-MY-002-DIVIDER-ROUTE/WorkBuddy` | 80949 | 2026-11-20T17:24:34.781457+00:00 |
| ZiniaoAgent | `SIM-002-MY-94adb6a537-TEST-MY-002-DIVIDER-ROUTE/ZiniaoAgent` | 80950 | 2026-11-20T17:24:34.852255+00:00 |

| 环节 | 日志序号 | 核验状态 | 本地耗时 ms |
| --- | --- | --- | --- |
| STEP01 选品研判 | 1 | VERIFIED | 0.772 |
| STEP02 市场与竞品分析 | 4 | VERIFIED | 0.048 |
| STEP03 商品素材规划 | 7 | VERIFIED | 0.299 |
| STEP04 英文标题与五点 | 10 | VERIFIED | 0.049 |
| STEP05 合规校验 | 13 | VERIFIED | 0.412 |
| STEP06 模拟节点分发 | 16 | VERIFIED | 287.955 |

各环输入输出通过上游事件号和摘要关联。三节点保存了同任务、同 SKU 的实际模拟回执。 [节点逐项回执](../node-receipts.jsonl)
