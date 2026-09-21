# TASK 工作区

## 挂科与重修记录

按教务系统截图整理的挂科 / 重修报名记录。

**主文件：** [`records/failed-courses/挂科与重修记录.md`](records/failed-courses/挂科与重修记录.md)

- 结构化数据：[`records/failed-courses/courses.json`](records/failed-courses/courses.json)
- 截图证据：`records/failed-courses/screenshots/`

当前已录入：本学期教务系统已报名的 3 门重修课（大学英语 I、计算机组成原理、毛概）。

---

## HYPE 中长期研究备忘

按用户提供的交易所截图思路整理的独立研究文档，交叉验证公开信息后补充容易漏看的变量。

**主文件：** [`reports/HYPE中长期分析_到200美元困难度与币本位合约选择_2026-09-19.pdf`](reports/HYPE中长期分析_到200美元困难度与币本位合约选择_2026-09-19.pdf)

覆盖内容：

1. 把截图翻译成可计算的价格、市值、解锁口径  
2. Hyperliquid 平台独特性与代币机制  
3. 到 200 美元的估值算术、情景带与困难度  
4. 平台发展前景（HIP-3 / HIP-4 / HyperEVM / 监管 / 竞争）  
5. 容易漏看的供应、收入分流、集中度与杠杆风险  
6. 下次回调开多：币本位 vs U 本位  
7. 总结  

本文是研究备忘，不是投资建议。

## 重新生成 PDF

```bash
pip install reportlab matplotlib
python3 scripts/generate_hype_report.py
```
