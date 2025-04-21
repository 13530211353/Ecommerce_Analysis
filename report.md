# 电商数据分析报告

## 概述
分析了在线零售数据集，旨在优化销售和客户参与。

## 方法论
- **数据清洗**：移除缺失值、取消订单和负值数据。
- **分析内容**：
  - 2010 年 12 月至 2011 年 12 月的 GMV 趋势。
  - RFM 客户分群。
  - 畅销商品分析。
- **工具**：Python、Pandas、Matplotlib、Seaborn。

## 发现
- **GMV**：2011 年 GMV 增长 109%，11 月达到峰值（115 万英镑）。
- **客户**：Top 20% 客户贡献约 80% GMV（待确认）。
- **商品**：“PAPER CRAFT, LITTLE BIRDIE”销售额约 16 万英镑。

## 可视化
- [月度 GMV 趋势](figures/monthly_gmv_trend.png)
- [客户消费金额分布](figures/monetary_distribution.png)
- [销售额 Top 10 商品](figures/top_10_products.png)
- [12 月每日 GMV 和订单量](figures/december_gmv_orders.png)

## 建议
- 增强 11 月节假日促销。
- 为高价值客户推出忠诚计划。
- 优化畅销商品库存。

## 数据局限性
- 2010 年 12 月：缺失 24-31 日数据。
- 2011 年 12 月：缺失 10-31 日数据，低估节假日销售。