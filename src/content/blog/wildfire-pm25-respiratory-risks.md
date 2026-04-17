---
title: '野火PM 2.5 在多个国家和地区引发的呼吸道风险'
description: '野火PM2.5对呼吸系统疾病住院风险的影响研究'
pubDate: '2024-03-21'
authors:
  - shouyu
toc: true
tags:
  - 随笔
  - 野火
  - 呼吸道健康
  - PM2.5
---

## 摘要

短期的野火暴露在对不同地区、不同人群呼吸系统疾病住院风险的影响

## 正文

**期刊**：Nature Sustainability

**DOI**：https://doi.org/10.1038/s41893-025-01533-9

**关键词**：野火、PM2.5、呼吸道疾病

**声明**：本文坚持一个中国原则，对于原文献中的错误会在首次出现时注明，后续不再注明。

## 文章速看

## 1. 科学问题

核心目标是 全面评估短期暴露于野火特定PM2.5对不同地区、不同人群呼吸系统疾病住院风险的影响 。具体来说，四点：

* 评估风险关系：量化野火特定PM2.5浓度与多种呼吸系统疾病（包括全因呼吸系统疾病、哮喘、慢性阻塞性肺病(COPD)、急性上呼吸道感染(AURI)、流感和肺炎）住院风险之间的浓度-反应（C-R）关系

* 识别脆弱人群：确定在性别、年龄、社区收入水平和社区非野火PM2.5污染水平等方面，哪些人群对野火烟雾的健康影响更为敏感或脆弱

* 量化疾病负担：估算由野火特定PM2.5导致的呼吸系统疾病住院负担，并分析其在不同国家和地区、不同时期的时空分布趋势

* 比较不同来源PM2.5的影响：直接比较野火产生的PM2.5与非野火源（如城市交通、工业排放）产生的PM2.5在导致呼吸系统疾病住院风险和负担上的差异

## 2. 研究数据

## 3. 研究方法

**两阶段时间序列分析框架**。常用于环境流行病学，以模拟来自多个社区的大规模、异质数据。这种方法允许对社区特定特征进行单独建模，保留关键的地方细微差别，并减轻将不同数据汇总到单一模型中可能产生的潜在偏差

### 3.1 统计单元

* "社区"。覆盖了8个国家和地区的1,052个社区  。这里的社区其实不是真正意义上的类似于我们国家的社区，而是受限于各个国家和地区的数据不同。而呈现出不同的行政区划。

> [!WARNING]
原文献中将台湾列为8个国家和地区之一，这严重违反了一个中国原则，本文后续将称为"中国台湾"。

### 3.2 变量定义

* 因变量 ：在每个社区，因变量是按病因分类的每日呼吸系统疾病住院人数。具体包括：

全因呼吸系统疾病
哮喘
慢性阻塞性肺病
急性上呼吸道感染
流感
肺炎

* 全因呼吸系统疾病

* 哮喘

* 慢性阻塞性肺病

* 急性上呼吸道感染

* 流感

* 肺炎

* 自变量：核心暴露变量是 每日野火特定PM2.5浓度 。

* 协变量/混杂因素：为了得到更准确的暴露-反应关系，模型控制了多种可能影响住院率的因素：

气象因素：日平均温度和相对湿度。
其他污染源：每日非野火源PM2.5浓度（non-wldf PM2.5）。
时间趋势：长期趋势、季节性变化和星期几效应（DOW）。

* 气象因素：日平均温度和相对湿度。

* 其他污染源：每日非野火源PM2.5浓度（non-wldf PM2.5）。

* 时间趋势：长期趋势、季节性变化和星期几效应（DOW）。

### 3.3 研究步骤与数学模型

整个分析过程分为两步：

#### 第一阶段：社区层面的时间序列分析

为1,052个社区中的每一个都单独拟合了一个时间序列模型，以估计该社区野火PM2.5暴露与每日住院人数之间的关系。他们使用的是**带有分布滞后非线性模型的准泊松回归**。

其核心模型公式如下 ：

* $\mu{}$：第 i个社区在第 t 天的预期住院人数。

* $cb(...)$：这是一个交叉基函数，用于同时灵活地模拟暴露（PM2.5浓度）和滞后（lg）两个维度上的非线性关系。这里，暴露维度被设置为线性，而滞后维度（从当天到过去7天）则通过对数尺度上的等距节点来构建 。

* $ns(...)$：这是一个自然立方样条函数，用于控制温度（Tmp）、相对湿度（RH）以及长期和季节性时间趋势（Tm）的非线性混杂效应 。d.f.是自由度。

* $\text{DOW}{}$：代表星期几的分类变量，用于控制每周的规律性波动 。

* $\alpha$：模型的截距项。

* 模型还纳入了非野火PM2.5浓度作为混杂因素进行调整 。

初步分析显示，住院风险在暴露当天（lg 0）和前一天（lg 1）最高，之后迅速减弱 。因此，最终分析集中在**滞后0-1天的累积相对风险**上 。

#### 第二阶段：多社区效应的合并

在获得每个社区的效应估计值后，研究者采用**随机效应元分析模型**将这些社区层面的结果在国家/地区层面进行合并，最终得到各个国家/地区以及所有研究区域总体的平均效应估计值 。这种方法考虑并量化了不同社区之间效应的异质性 。

通过这个两阶段框架，研究不仅得出了每增加1 mugm˜−3 野火PM2.5对应的住院风险增加百分比，还绘制了如图2所示的集合浓度-反应（C-R）曲线，直观展示了住院风险如何随PM2.5浓度升高而变化 。

## 3. 研究结果

加拿大、巴西、新西兰、泰国、澳大利亚、智利、越南和中国台湾在 2000-2019 年间 1052 个研究社区中平均每日特定野火 PM 2.5 （µg/m −3 ）的空间分布。

在滞后 0-1 天内，野火 PM 2.5 暴露的呼吸住院风险的累积风险曲线。

* 显著的健康风险：研究发现，野火特定PM2.5浓度每增加1 $\mu g~m^{-3}$，全因呼吸系统疾病、哮喘、COPD、AURI、流感和肺炎的住院风险分别显著增加0.36%, 0.48%, 0.38%, 0.42%, 0.79%和0.36% 。流感住院风险的关联性最强 。

* 脆弱人群特征：年龄在19岁及以下或60岁及以上的人群 、来自低收入社区的人群  以及居住在非野火PM2.5背景污染水平较高地区的人群  表现出更高的住院风险。

* 显著的地理差异：不同国家和地区的风险存在差异。例如，巴西、泰国、中国台湾和越南的居民面临的总体风险更高 ；而澳大利亚和新西兰的哮喘住院风险与野火PM2.5的关联性更强 。

* 野火PM2.5的危害性更大：与非野火源的PM2.5相比，野火特定PM2.5对所有研究的呼吸系统疾病都构成了更大的住院风险 。

* 疾病负担归因：尽管野火源PM2.5在总PM2.5浓度中占比不大（中位数为1.4 mugm˜−3 v 非野火源的13.4 $\mu g~m^{-3}$），但其对PM2.5相关呼吸系统住院的贡献却高达42.4% 。每年，估计有25,321例全因呼吸系统住院可归因于野火特定PM2.5 。

* 时空趋势变化：从2000年到2019年，由野火PM2.5导致的全因呼吸系统住院归因比例（AF）在澳大利亚、加拿大、智利、新西兰和中国台湾等地呈现总体上升趋势 ，而在巴西和越南则有所下降 。

## 4. 创新点

* 规模大时间跨度长：这是迄今为止关于野火特定PM2.5与特定原因呼吸系统住院关系的最大规模研究 。它覆盖了八个不同社会经济和环境背景的国家与地区，数据时间跨度长达20年，这使其结论具有更强的普遍性和稳健性 。

* 深入的时空负担评估：文章不仅评估了风险，还量化了疾病负担（归因分数和人数），并分析了这些负担在过去二十年间的时空演变趋势 。这为理解野火空气污染影响的动态演变提供了重要视角，对政策制定和资源分配极具价值 。

* 识别脆弱群体与地区：通过详细的分组分析，研究精准地识别出了风险最高的脆弱人群和地区，为制定有针对性的公共卫生干预措施和解决环境不公问题提供了科学依据 。

## 文章构思

## 5. 摘要

摘要共八句话，202个单词

1. Under a warming climate, wildfires are becoming more frequent and  severe.  背景？ 什么背景下什么问题在变得严重。

1. Multicountry studies evaluating associations between wildfire  fine particulate matter (PM2.5) and respiratory hospitalizations are lacking. 研究空白？ 缺乏什么什么研究。

Here we evaluate the short-term effects of wildfire-specific PM2.5 on respiratory hospitalizations from 1,052 communities across  Australia, Brazil, Canada, Chile, New Zealand, Vietnam, Thailand and  Taiwan, during 2000–2019. 做了什么事？ 评估了 什么时间 什么地区 什么灾害 对 什么 的影响。

1. Here we evaluate the short-term effects of wildfire-specific PM2.5 on respiratory hospitalizations from 1,052 communities across  Australia, Brazil, Canada, Chile, New Zealand, Vietnam, Thailand and  Taiwan, during 2000–2019. 做了什么事？ 评估了 什么时间 什么地区 什么灾害 对 什么 的影响。

1. A 1 µg m−3 increase in wildfire-specific PM2.5 was associated with increased hospitalization risks for all-cause  respiratory, asthma, chronic obstructive pulmonary disease, acute upper  respiratory infection, influenza and pneumonia by 0.36%, 0.48%, 0.38%,  0.42%, 0.79% and 0.36%, respectively. 结论一：总体，某种灾害每增加多少，导致什么风险增加多少

1. Higher risks were observed among  populations ≤19 or ≥60 years old, from low-income or high non-wildfire  PM2.5 communities, and residing in Brazil, Thailand, Taiwan and Vietnam.  Australia and New Zealand exhibited a greater hospitalization risk for  asthma associated with wildfire-specific PM2.5. 结论二：弱势群体 风险？

1. Compared with non-wildfire PM2.5, wildfire-specific PM2.5 posed greater hospitalization risks for all respiratory diseases and a greater burden of asthma. 结论三： 主题，野火和非野火PM2.5风险对比

1. Wildfire-specific PM2.5 contributed to 42.4% of PM2.5-linked respiratory hospitalizations, dominating in Thailand. 结论四： 以某个突出的地区为例说明风险

1. Overall, the substantial contribution of wildfire-specific PM2.5 to respiratory hospitalizations demands continued mitigation and  adaptation efforts across most countries. 政策建议：应采取行动

1. Intervention should be  prioritized for influenza, children, adolescents, the elderly and  populations in low-income or high-polluted communities. 采取行动应偏向 弱势群体

套路：背景-研究空白-总体结论-公平性结论-主题结论-突出某特别地区-政策-政策建议

## 6. Main

第一段，**说明野火在全球呈上升趋势**"2023 年，加拿大。美欧。到 21 世纪末，全球易燃面积预计将增加 29%"，有背景事实也有相关文献的预测。这两点可以结合说明某种灾害的严重性。最后一句话话锋一转，通过**野火影响健康组成因素转到PM2.5**，启发下文。

In recent decades, wildfires, encompassing all types of fire in  vegetated landscapes, have been**increasingly reported worldwide**. This  trend is**particularly evident**in Australia, the Brazilian Amazon,  Europe, Russia, Canada and the western United States1. Notably, Canada experienced a**record-breaking**series of wildfires in 2023, which burned an estimated 185,000 km2, impacting all provinces and territories2.**Severe**wildfires were also experienced in the United States and Europe during the 2023 fire season3. Climate change is expected to increase the frequency, duration and intensity of extreme wildfire events4. The global fire-prone area is projected to increase by 29%, by the end of the twenty-first century5. This may result in amplified socioeconomic and health burdens6. Wildfires harm human health primarily through wildfire smoke (for  example, toxic gases and particles), of which ~90% of the total particle mass is comprised of fine particulate matter with diameters ≤2.5 µm (PM2.5)7.

第二段，**主要说明研究空白**。通过与普通PM2.5的对比，引出野火的PM2.5可能构成更大的伤害，尤其是呼吸道。随后开始说明当前研究空白。以下句式很好用 "**尽管**.....，**但**...的研究**仍然有限**。**先前的研究**大多**...，**重点关注... 。可能阻碍了研究结果...的普遍适用性。此外.... 截至目前，仅有...。一项研究...，另一项...""   这部分主要说明了几个空白：1 没有跨国研究；2疾病单一；3针对群体单一

**Compared to**urban-sourced PM2.5, the higher submicronic particle content8and distinct chemical composition of wildfire-specific PM2.5 probably contribute to its**increased toxicity**at equivalent doses1, potentially posing a**greater threat**to human health, with respiratory complications**as a particular concern**6,9.**Despite**the**substantial burden**of wildfire-related health impacts on low- and middle-income countries (LMICs)10, research investigating the health consequences of wildfire-specific PM2.5 in these regions**remains surprisingly limited**.**Previous investigations**have largely been conducted in high-income countries, such as the United States and Canada, focusing on a specific local area or fire event9,11,12,13,14,15,16,17. This focus**potentially hinders**the generalizability of findings to  other countries disproportionately burdened by wildfires, such as Chile  and Brazil.**Furthermore**, studies in LMICs**are imperative to**inform  targeted intervention and resource allocation directed towards areas  with the greatest need, ultimately contributing to global health equity.**To date**,**only**two multicountry studies have investigated the impacts of wildfire-specific PM2.5 on respiratory health. One investigated a single outcome (acute respiratory infection) within a specific population (children)18and the other one focused**solely**on all-cause respiratory mortality19,**without covering**other major types of respiratory diseases.

第三段，**进一步说明研究空白**。 "时空负担，异质建模方法，野火和非野火 PM2.5  暴露之间关联对比。" 这三者空白也对应了后续的研究内容。  这段的基本句式就是" 很少有研究...，这什么缺陷。进一步的，先前的研究...，这有什么缺陷或挑战。最后，很少有...。因此，有必要....(总结针对这些空白要做什么)"

**Additionally**,**few**multicountry studies have quantified the  spatiotemporal burden of respiratory diseases attributable to  wildfire-specific PM2.5, which**limits**their ability to account for the dynamic vulnerability of  populations over time.**Further**, previous investigations used  heterogeneous modelling approaches. This poses**methodological challenges**in establishing a more representative association between short-term  wildfire-specific PM2.5 exposure and respiratory diseases.**Finally**,**few**existing literature  compared the association of respiratory hospitalizations with wildfire  and non-wildfire PM2.5 exposure.**Therefore**, a systematic analysis of the risks and burden of  cause-specific respiratory diseases associated with wildfire-specific PM2.5**is warranted**, to provide**more comparable evidence**, by applying a unified analytic framework to different communities.

第四段。利用什么数据，**研究目标/科学问题是什么？**1，2，3，4.

**Here**, by**leveraging**hospitalization data from eight countries and  territories, over 20 years, we**aimed to**: (1) characterize the  concentration–response (C–R) relationship between wildfire-specific PM2.5 and hospitalization risks for all-cause respiratory, asthma, chronic  obstructive pulmonary disease (COPD), acute upper respiratory infection  (AURI), influenza and pneumonia; (2) identify vulnerable populations;  (3) quantify the spatiotemporal trends of respiratory hospitalizations  attributable to wildfire-specific PM2.5; and (4) compare the health impacts of wildfire and non-wildfire PM2.5 on respiratory hospitalizations.

## 7. Methods

### 7.1 医院住院和社会经济数据

第一段 说明了医院住院数据的基本情况，包括地理范围，社区数量，面积，人口，时间跨度。具体的数据收集、ICD 代码和数据覆盖的详细信息放到了补充材料里。因为数据来自不同的国家和地区，不同的医院，不同的部门，不同的行政区划级别，在补充材料里细说了。

第二段 说明了 GDP和GPW的处理和分类情况，非野火 PM 2.5 浓度的分类情况。详细放在补充材料里。

第三段 说明了对基础数据集进行了特征描述。就是类似于极限表一样的。不过是按照以年龄、性别、社区收入水平、社区非野火 PM2.5 水平和国家及地区为特征进行了统计描述----两张表。放在补充材料里：表S1. 研究期间八个国家/地区空间单元概况、研究社区数量及野火相关PM2.5日均浓度估算值（微克/立方米）。表S2。研究期间不同呼吸道疾病病因导致的各亚组年度及日均呼吸系统住院病例数（N）。

### 7.2 野火导致的PM2.5 和气象数据

这两段说明了特定野火 PM 2.5 的日浓度和气象数据情况

一般来说对于数据的详细处理尽量在补充材料里面细说。

### 7.3 统计分析

首先第一段，一两句话说明分析思路是怎样的，模型是什么。然后一句话说明一下模型的定义，一句话说明优势。并且可以在补充材料中详细说明选择这种方法的原因和方法的优势。

第二段。第一阶段在每个社区上使用准泊松回归和分布滞后非线性模型，说明参数含义和选择原因。

第三段。第二阶段随机效应元分析模型。

第三段。确定并验证"剂量-反应关系"的形状

第四段。通过分组（亚组分析）的方法，分别考察野火PM2.5对不同年龄、性别、社区收入和背景污染水平人群的影响是否存在差异 。

第五段。将相对风险转化为实际的健康影响，即计算出到底有多少住院病例和多大比例的住院（Attributable Fraction, AF）可以归因于野火PM2.5的暴露。使用蒙特卡洛模拟来评估这些负担估算值的不确定性，并进一步分析了这些负担在2000年至2019年间是如何随时间演变的。

第六段。对非野火PM2.5重复了与野火PM2.5完全相同的分析流程，估算了其导致的住院风险和疾病负担。比较两者的效应大小和归因于它们的住院比例差异（AF difference）

第七段。R软件版本和包使用情况。

第八段。伦理批准。

## 8 Results

### 8.1 摘要统计

第一段。数据集的基本描述。通过补充表1和表2。 这两张表没放到正文，而是放了一张地图，来说明灾害--野火导致PM2.5浓度的分布。比放表更好看。

### 8.2 呼吸住院风险和野火相关 PM 2.5

第二段。第一阶段的结果说明。放到扩展数据中。野火 PM 2.5 在当前日和前一天（滞后 0 和滞后 1）持续产生升高的呼吸系统住院风险

第三段。回应了第一个科学问题：C-R关系。野火 PM 2.5 与滞后 0-1 天呼吸系统住院之间的累积 C-R 关系，线性或超线性

第四段。回应了第一个科学问题：野火相关的的 PM 2.5 与所有考察的呼吸系统住院之间存在一致的积极关联。

**与野火相关PM2.5暴露浓度每增加1微克/立方米相关的特定呼吸系统疾病住院累积相对风险（95%置信区间）**

第五段。回答了第二个科学问题：识别脆弱人群。年龄、社区收入水平、社区非野火 PM 2.5 水平和国家或地区改变了野火特定 PM 2.5 与呼吸系统住院风险之间的关联

**与野火特定 PM 2.5 在滞后 0-1 天内增加 1 µg m −3 相关的呼吸道住院的累积相对风险。**

### 8.3 年度归因负担

这一段回答了第三个科学问题：**量化疾病负担**。

**与野火相关PM2.5暴露在滞后0-1天期间，按社区收入水平及国家和地区划分的特定病因呼吸系统住院年归因病例数（N，95%置信区间）**

### 8.4 野火导致的PM 2.5 与非野火 PM 2.5 的比较

这里回答了第四个科学问题：**比较不同来源PM2.5的影响**

第一段。与非野火污染源相比，野火仅占环境PM2.5的小部分（17.1%）。然而，相较于非野火PM2.5，野火特有PM2.5与显著更高的风险相关，并且在所研究的所有主要呼吸系统疾病住院病例中占据了相当大的比例（图4及附表10和11）。

第二段。野火相关的PM2.5导致的呼吸道住院 AF的时空模式存在差异。整体上，地区之间的不同。

第三段。不同地区野火和非野火导致的AF发展模式和差异。

## 9 讨论

这篇篇幅太长了，下篇论文再针对性的解析引言和讨论如何构思的吧