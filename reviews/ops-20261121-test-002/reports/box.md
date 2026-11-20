# 带盖可叠放收纳盒 · 单品模拟连通报告

任务 `OPS-20261121-TEST-002` · SKU `TEST-MY-002-BOX` · MY / SIM-MY-002 · MYR。本品六环记录 6 条，节点回执 3 份，主批分发结果为 VERIFIED。 [总报告](../report.md)

## 1　选品与日常款测算

家居收纳。合成产品含包装 680 g，单件上限 2,500 g。模拟成本来源为本单夹具，到仓 CNY 14.00；按模型计入物流和其他单件成本后为 MYR 22.54。真实货源、毛利、实物尺寸及材质、商标及销售辖区证据均待核实。

| 含税面价 MYR | 商家 8% 券后实付 MYR | 扣税净收入 MYR | 毛利率 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 54.90 | 50.51 | 45.92 | 50.92% | 10.25 |

毛利率分母是扣税净收入，精确百分数为 8786900/172569。按未舍入值检查 8% 日常门槛。三种日常场景与费项明细见 STEP01。[流程日志](../flow.jsonl)

## 2　市场与竞品分析

模拟马来语搜索词 **kotak bertutup boleh susun**。统计窗为 2026-10-24 至 2026-11-20（28天），虚构搜索 56 次、商品点击 15 次。每款一个模拟对照，未观测市场销量或买家评论。

本地模拟对照 SIM-MY-COMP-BOX 为模拟无盖开口筐，售价 MYR 39.90。其特征为无盖开口，取用时无需移开盖子。

预设使用场景为小空间柜架中按层归置物品，希望能看见盒内物件。买前问题为“盒盖如何定位上一层，尺寸指盒内空间还是外部尺寸？”

## 3　素材规划、示意图与权利记录

本 SKU 的展示计划为“示意图以剖开的叠放轮廓突出盖边与盒底，标清外部尺寸，单件含一盒一盖。”
本地按商品几何轮廓绘制 320 × 240 SVG，版本 v1。图内没有照片、外部图像、字体或音轨。

![带盖可叠放收纳盒的合成结构示意图](../assets/test-my-002-box.svg)

测试许可 `SIM-LIC-TEST-MY-002-BOX`，范围 `simulated-commercial-review-only`，地区 MY，有效期 2026-11-01 至 2026-12-31。核验图像 SHA-256 为 `3c597f49aae1cc37a9e5881ca6a8631c3503378add325b28dfe3110536950693`。 [许可登记](../assets/test-my-002-box.licence.json)

## 4　英文标题与五点

**Clear Stackable Storage Box with Removable Lid**

1. One clear box with a separate, removable lid.
2. External dimensions are 30 cm long, 20 cm wide and 12 cm high.
3. The recessed lid rim locates the base of a matching box when stacking.
4. A clear body lets you see the contents from the side.
5. Measure the shelf depth and leave room above to lift off the lid.

模拟稿版本 v1，文本 SHA-256 为 `5568bec6f440528355929571efadb328263b96983eb21640f8c8fa1128e6dfcd`。实店文案待补适用规则及实物依据。

## 5　四项合规核验

R10 图片测试许可通过。R05 在马来站为不适用，核查 UK 在售 SKU 0 个，更新 UK 全量基线为否。P0 主批冻结为否。本次门禁仅放行测试包。

R03 的模拟秒杀价为 MYR 46.67，每人限购 1，活动配额 3。两种情景均纳入同一时点前台快照的自动券。

| 情景 | 券后买家付款 MYR | 毛利率 | 专用底线 | 扣费后单件利润 MYR |
| --- | --- | --- | --- | --- |
| 误叠商家 8% 券 | 41.94 | 40.89% | 13.00% | 4.60 |
| 排除商家 8% 券 | 45.67 | 45.72% | 13.00% | 7.06 |

R03 主批核验通过，活动提交为否。在分离的故障试验中，对本 SKU 的投递尝试被拒 1 次。[风险探针日志](../risk-probes.jsonl)

## 6　三节点签收与回读

同一请求 `SIM-002-MY-94adb6a537-TEST-MY-002-BOX-ROUTE`。WorkBuddy 核对 754 字节图片正文、5 条英文要点及原稿版本。妙手返回模拟店号 `SIM-MIAO-MY-002`、采集箱对象 `SIM-BOX-002-02`，对象状态 SIMULATED_UNPUBLISHED，本次商品草稿号未生成。紫鸟模拟环境为 `SIM-ZN-MY-002`，入场检查 9/9 项通过。

| 节点 | 回执 ID | 接收进程 PID | 回执时间 |
| --- | --- | --- | --- |
| MiaoshouERP | `SIM-002-MY-94adb6a537-TEST-MY-002-BOX-ROUTE/MiaoshouERP` | 80952 | 2026-11-20T17:24:34.995113+00:00 |
| WorkBuddy | `SIM-002-MY-94adb6a537-TEST-MY-002-BOX-ROUTE/WorkBuddy` | 80953 | 2026-11-20T17:24:35.064854+00:00 |
| ZiniaoAgent | `SIM-002-MY-94adb6a537-TEST-MY-002-BOX-ROUTE/ZiniaoAgent` | 80954 | 2026-11-20T17:24:35.135015+00:00 |

| 环节 | 日志序号 | 核验状态 | 本地耗时 ms |
| --- | --- | --- | --- |
| STEP01 选品研判 | 2 | VERIFIED | 1.051 |
| STEP02 市场与竞品分析 | 5 | VERIFIED | 0.035 |
| STEP03 商品素材规划 | 8 | VERIFIED | 0.222 |
| STEP04 英文标题与五点 | 11 | VERIFIED | 0.040 |
| STEP05 合规校验 | 14 | VERIFIED | 0.256 |
| STEP06 模拟节点分发 | 17 | VERIFIED | 282.732 |

各环输入输出通过上游事件号和摘要关联。三节点保存了同任务、同 SKU 的实际模拟回执。 [节点逐项回执](../node-receipts.jsonl)
