# 柜门双钩挂篮 · 单品模拟连通报告

任务 `OPS-20261121-TEST-002` · SKU `TEST-MY-002-HANGER` · MY / SIM-MY-002 · MYR。本品六环记录 6 条，节点回执 3 份，主批分发结果为 VERIFIED。 [总报告](../report.md)

## 1　选品与日常款测算

家居收纳。合成产品含包装 420 g，单件上限 2,500 g。模拟成本来源为本单夹具，到仓 CNY 12.00；按模型计入物流和其他单件成本后为 MYR 17.83。真实货源、毛利、实物尺寸及材质、商标及销售辖区证据均待核实。

| 含税面价 MYR | 商家 8% 券后实付 MYR | 扣税净收入 MYR | 毛利率 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 44.90 | 41.31 | 37.55 | 52.52% | 8.89 |

毛利率分母是扣税净收入，精确百分数为 22238200/423407。按未舍入值检查 8% 日常门槛。三种日常场景与费项明细见 STEP01。[流程日志](../flow.jsonl)

## 2　市场与竞品分析

模拟马来语搜索词 **bakul gantung pintu kabinet**。统计窗为 2026-10-24 至 2026-11-20（28天），虚构搜索 34 次、商品点击 9 次。每款一个模拟对照，未观测市场销量或买家评论。

本地模拟对照 SIM-MY-COMP-HANGER 为模拟台面置物篮，售价 MYR 32.90。其特征为独立平底设计，占用台面。

预设使用场景为柜内侧利用门板挂放小件，须先核对门厚及闭门间隙。买前问题为“挂钩能否跨过门板，装上后是否还能关门？”

## 3　素材规划、示意图与权利记录

本 SKU 的展示计划为“侧面图突出双钩固定方式；文案给出门板厚度上限并提示自行核对闭门空间。”
本地按商品几何轮廓绘制 320 × 240 SVG，版本 v1。图内没有照片、外部图像、字体或音轨。

![柜门双钩挂篮的合成结构示意图](../assets/test-my-002-hanger.svg)

测试许可 `SIM-LIC-TEST-MY-002-HANGER`，范围 `simulated-commercial-review-only`，地区 MY，有效期 2026-11-01 至 2026-12-31。核验图像 SHA-256 为 `f45e3ec6da39427463cf01fd9ae3e92a6c9cbf4ac5e77ec4e3c5dd6fc5e08f1a`。 [许可登记](../assets/test-my-002-hanger.licence.json)

## 4　英文标题与五点

**Over-Cabinet-Door Wire Basket with Two Hooks**

1. One wire basket with two hooks that fit over a cabinet door.
2. Basket dimensions are 22 cm wide, 10 cm deep and 18 cm high.
3. The hooks fit a door up to 18 mm thick.
4. Check the clearance above and behind the door before fitting.
5. The open basket provides a place for small household items.

模拟稿版本 v1，文本 SHA-256 为 `1e12df9aa8bc052614d13bbee506683122b9f1853496b441542663a496b14310`。实店文案待补适用规则及实物依据。

## 5　四项合规核验

R10 图片测试许可通过。R05 在马来站为不适用，核查 UK 在售 SKU 0 个，更新 UK 全量基线为否。P0 主批冻结为否。本次门禁仅放行测试包。

R03 的模拟秒杀价为 MYR 38.17，每人限购 1，活动配额 3。两种情景均纳入同一时点前台快照的自动券。

| 情景 | 券后买家付款 MYR | 毛利率 | 专用底线 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 误叠商家 8% 券 | 34.12 | 42.51% | 13.00% | 4.16 |
| 排除商家 8% 券 | 37.17 | 47.24% | 13.00% | 6.17 |

R03 主批核验通过，活动提交为否。在分离的故障试验中，对本 SKU 的投递尝试被拒 1 次。[风险探针日志](../risk-probes.jsonl)

## 6　三节点签收与回读

同一请求 `SIM-002-MY-94adb6a537-TEST-MY-002-HANGER-ROUTE`。WorkBuddy 核对 812 字节图片正文、5 条英文要点及原稿版本。妙手返回模拟店号 `SIM-MIAO-MY-002`、采集箱对象 `SIM-BOX-002-03`，对象状态 SIMULATED_UNPUBLISHED，本次商品草稿号未生成。紫鸟模拟环境为 `SIM-ZN-MY-002`，入场检查 9/9 项通过。

| 节点 | 回执 ID | 接收进程 PID | 回执时间 |
| --- | --- | --- | --- |
| MiaoshouERP | `SIM-002-MY-94adb6a537-TEST-MY-002-HANGER-ROUTE/MiaoshouERP` | 80956 | 2026-11-20T17:24:35.277096+00:00 |
| WorkBuddy | `SIM-002-MY-94adb6a537-TEST-MY-002-HANGER-ROUTE/WorkBuddy` | 80957 | 2026-11-20T17:24:35.346697+00:00 |
| ZiniaoAgent | `SIM-002-MY-94adb6a537-TEST-MY-002-HANGER-ROUTE/ZiniaoAgent` | 80958 | 2026-11-20T17:24:35.416400+00:00 |

| 环节 | 日志序号 | 核验状态 | 本地耗时 ms |
| --- | --- | --- | --- |
| STEP01 选品研判 | 3 | VERIFIED | 1.360 |
| STEP02 市场与竞品分析 | 6 | VERIFIED | 0.038 |
| STEP03 商品素材规划 | 9 | VERIFIED | 0.258 |
| STEP04 英文标题与五点 | 12 | VERIFIED | 0.047 |
| STEP05 合规校验 | 15 | VERIFIED | 0.237 |
| STEP06 模拟节点分发 | 18 | VERIFIED | 281.661 |

各环输入输出通过上游事件号和摘要关联。三节点保存了同任务、同 SKU 的实际模拟回执。 [节点逐项回执](../node-receipts.jsonl)
