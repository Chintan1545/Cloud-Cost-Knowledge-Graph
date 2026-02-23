# Test Queries Documentation

## 1. Which service costs most?

Retrieval: Graph Aggregation  
Method: SUM(billedCost) GROUP BY Service  

Result: VM service highest cost.

---

## 2. Compare AWS and Azure costs

Retrieval: Graph query with vendor filter  

---

## 3. Top Production Azure Resources

MATCH (c:CostRecord)
WHERE c.vendor = "Azure"
AND c.environment = "Production"

---

## 4. Commitment Utilization

Exclude chargeCategory = "Commitment Purchase"

---

## 5. Which cost type to analyze spend?

Use EffectiveCost for actual spend.