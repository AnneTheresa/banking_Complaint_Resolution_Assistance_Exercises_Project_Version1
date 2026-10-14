# Assisted Journey

## Objective

Show how the Banking Complaint Resolution Assistant supports complaint handling while maintaining human accountability.

---

## Stage 1 — Complaint Intake

**Reference:** Spec Flow 1  
**Human responsibility:** Customer submits complaint.

**AI assistance**

- Extract complaint facts
- Suggest category
- Suggest urgency
- Identify missing information

**Structured data (SQL):** None  
**Generated assistance:** Classification recommendation  
**Final decision:** Complaint Analyst

---

## Stage 2 — Complaint Review

**Reference:** Spec Flow 2  
**Human responsibility:** Analyst reviews complaint.

**SQL facts**

- Customer history
- Complaint history
- Account information
- Service requests

**AI assistance:** Evidence organization  
**Generated assistance:** Evidence summary  
**Final decision:** Complaint Analyst

---

## Stage 3 — Policy Retrieval

**Reference:** Spec Flow 2

**Document retrieval**

- Complaint procedures
- Banking policies
- Escalation guidance

**AI assistance:** Find relevant policies  
**Generated assistance:** Policy summary with references  
**Final decision:** Complaint Analyst

---

## Stage 4 — Investigation Assessment

**Reference:** Spec Flow 2

**SQL facts:** Customer records  
**Document retrieval:** Policy information  
**AI assistance:** Highlight evidence gaps  
**Generated assistance:** Investigation summary  
**Final decision:** Complaint Analyst

---

## Stage 5 — Recommendation Drafting

**Reference:** Spec Flow 3

**SQL facts:** Retrieved evidence  
**Document retrieval:** Applicable procedures  
**Generated assistance:** Draft recommendation

**Important:** Recommendation is advisory only.  
**Final decision:** Complaint Analyst

---

## Stage 6 — Escalation Review

**Reference:** Spec Flow 4  
**Human responsibility:** Supervisor review

**SQL facts:** Complaint information  
**Document retrieval:** Policy references  
**AI assistance:** Provide decision context  
**Generated assistance:** Summary package  
**Final decision:** Supervisor

---

## Stage 7 — Resolution Approval

**Reference:** Spec Flow 4  
**Human responsibility:** Approve or reject recommendation.

**AI assistance:** None  
**Decision authority:** Supervisor

---

## Stage 8 — Audit and Closure

**Reference:** Audit Requirements  
**Human responsibility:** Finalize complaint.

**AI assistance:** Generate audit records  
**SQL facts:** Complaint outcome  
**Generated assistance:** Audit summary  
**Final decision:** Complaint Analyst
