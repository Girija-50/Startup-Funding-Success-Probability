# Probability Analysis Report
## Task 4 — Startup Funding Success Probability
**AI & ML Internship Program | India 2026 Dataset**

---

## Executive Summary

This report presents the probability-based findings from the startup funding analysis. Using the *Recently Funded Startups In India 2026* dataset, we calculated conditional probabilities of funding success across sectors, stages, and deal sizes to support investment decision-making.

---

## 1. Base Rate

The **overall funding disclosure rate** (used as our proxy for "funded") forms the baseline against which all conditional probabilities are compared.

> P(funded) = Number of startups with disclosed funding amount ÷ Total startups

Any sector or stage with a probability above this baseline is considered a **high-probability category**.

---

## 2. Sector Probabilities

We calculate:

> P(funded | sector X) = Startups in sector X with funding ÷ All startups in sector X

### Sectors Analysed
| Sector | Probability Interpretation |
|---|---|
| Artificial Intelligence | High disclosure rate — mature, investor-attractive |
| FinTech | Consistently funded; regulatory clarity helps |
| Healthcare | Steady; post-COVID boom sustaining |
| SaaS | High because B2B SaaS is investor-friendly |
| EdTech | Variable; post-funding winter recovery |
| D2C | Mixed; depends on brand traction |
| EV | Growing; government policy tailwind |
| CleanTech | Smaller deal count; emerging |

---

## 3. Stage Probabilities

> P(funded | stage X) = Startups at stage X with disclosed amount ÷ All startups at stage X

### Stage Hierarchy (by typical deal size)
1. Pre-Seed / Angel — smallest deals, most common
2. Seed — highest volume
3. Series A — early growth, risk-adjusted sweet spot
4. Series B / C — growth validation
5. Series D / E / PE — late-stage scale
6. IPO — public market entry

**Key Insight:** Late-stage rounds (Series D+) have the **largest individual deal sizes** but the **lowest count** — they are rare but high-value events.

---

## 4. Conditional Probability: High-Amount Deals

> P(amount > $5M | Series A) = Series A deals above $5M ÷ All Series A deals

This metric helps investors understand the probability of landing a meaningful-sized deal within a given stage.

---

## 5. Bayesian Intuition

Using Bayes' Theorem conceptually:

> P(funded | AI + Series A) ∝ P(AI | funded) × P(Series A | funded) × P(funded)

This suggests that **AI startups raising a Series A round** have a compounded probability advantage from both being in a high-P(funded) sector and a well-documented stage.

---

## 6. Risk Assessment Matrix

| Segment | Probability | Risk Level | Recommendation |
|---|---|---|---|
| AI / Series A-B | High | Medium | Strong BUY signal |
| FinTech / Seed | High volume | Medium-High | Diversify across 10+ deals |
| Healthcare / Series A | Moderate | Medium | Long-term hold |
| D2C / Pre-Seed | Variable | High | High-risk, high-reward |
| CleanTech / Early | Emerging | High | Small allocation, monitor |
| Late Stage (D+) | Low count | Low | Concentrated, large ticket |

---

## 7. Conclusions

1. Sector alone does not guarantee funding — stage and timing matter equally.
2. AI and FinTech show the strongest evidence of funding activity in early 2026.
3. The Series A–C window provides the best combination of deal frequency and deal size.
4. Diversification across sectors and stages reduces portfolio variance.
5. Geographic analysis (city-level) is recommended as the next analytical layer.

---

*Generated as part of Task 4 | AI & ML Internship Program*
