# Ontology Design – Cloud Cost Knowledge Graph

## Based on FOCUS 1.0 Specification (FinOps Foundation)

## Core Classes

- CostRecord
- Account
- TimeFrame
- Charge
- Resource
- Service
- Location
- VendorSpecificAttributes
- CostAllocation

## Class Hierarchy

VendorSpecificAttributes
  ├── AWS
  └── Azure

Account
  ├── BillingAccount
  └── SubAccount

## Object Properties

- (CostRecord)-[:HAS_SERVICE]->(Service)
- (CostRecord)-[:INCURRED_BY]->(Resource)
- (Resource)-[:DEPLOYED_IN]->(Location)
- (CostRecord)-[:HAS_CHARGE]->(Charge)

## Data Properties

- billedCost
- effectiveCost
- contractedCost
- currency
- consumedQuantity

## Cardinality Rules

- One CostRecord → One Service
- One Resource → Many CostRecords
- One Service → Many Resources

## Validation Rules

- billedCost ≥ 0
- chargeCategory ∈ {Usage, Commitment, Credit, Tax}
- effectiveCost = billedCost + amortizedCost

## Allocation Model

- allocationMethod: Proportional | EvenSplit | Weighted
- allocationTargetType: Application | CostCentre
- allocatedCost derived from cost pool