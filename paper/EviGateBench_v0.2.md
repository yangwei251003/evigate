---
title: "EviGateBench: An Evidence-Gated Protocol and Deterministic Reference-Controller Study for Research-Workflow Reliability"
status: "audited draft; not submission-ready"
study_classification: "synthetic deterministic reference-controller simulation"
---

# EviGateBench: An Evidence-Gated Protocol and Deterministic Reference-Controller Study for Research-Workflow Reliability

## Abstract

Research agents may complete long tasks without preserving evidence, provenance, or escalation boundaries. This paper introduces EviGateBench, a versioned synthetic benchmark protocol for three research-workflow policies: direct drafting, non-blocking linear processing, and evidence-gated processing. The protocol records citation-authenticity, claim-support, run-provenance, and escalation defects; it requires pre-run manifests, immutable raw outputs, and claim-to-evidence links. We executed 48 preregistered runs on 16 v0.2 packets using deterministic reference controllers. The direct controller detected and contained no seeded issues and continued unsafely in all runs. The linear controller detected all issues but continued unsafely in all runs. The EviGate controller detected and contained all issues without unsafe continuation. These outcomes validate that the harness distinguishes the intended scripted policies. They do not estimate the performance of large language model agents, humans, or real scientific workflows. Version 0.1 exposed answer information and is retained as a documented validity failure; v0.2 removes that leakage. EviGateBench is therefore a reproducibility-oriented protocol and harness, not evidence that evidence gates improve autonomous research agents generally.

**Keywords:** research agents; evidence provenance; workflow reliability; benchmark design; selective escalation; reproducibility.

## 中文摘要

研究智能体的长程任务完成度并不能自动证明其过程遵守证据、实验溯源与风险升级边界。本文提出 EviGateBench：一个小规模、可版本化的研究工作流可靠性基准协议。该基准以合成研究任务包检验直接起草、非阻断线性流程与证据门控流程；任务涵盖引用真实性、论断支持、运行溯源和需要人工升级的阻塞因素。基准要求预注册运行清单、不可覆盖的原始输出与论断—证据图。本文报告 v0.2 语料上的确定性参考控制器模拟，包含 16 个任务和 48 个预注册条件运行。直接控制器未检测或阻断任何植入问题，并在所有运行中不安全地继续；线性控制器检测到问题，但同样在所有运行中继续；EviGate 控制器检测并阻断或升级了全部问题。该结果仅验证基准工具链与评分规则能够区分预设的工作流策略，不能用于推断大语言模型、研究人员或真实科研工作流的表现。v0.1 语料曾暴露答案信息，已作为负面结果永久保留；v0.2 已移除该泄露。

**关键词：** 科研智能体；证据溯源；工作流可靠性；基准设计；选择性升级；可复现性。

## 1. Introduction

Research-oriented agents must coordinate literature, data, experiments, analysis, and writing. Existing evaluations demonstrate that such coordination is difficult. PaperBench evaluates agents attempting to replicate 20 ICML 2024 Spotlight and Oral papers and decomposes the work into 8,316 gradable tasks [@starace2025paperbench]. AgentBench likewise treats reasoning and decision-making in interactive environments as core evaluation targets [@liu2024agentbench]. These efforts motivate process-sensitive evaluation; neither is evidence that the present system is effective.

A complementary question is whether a workflow knows when progress should stop. HiL-Bench frames selective escalation as recognizing missing, ambiguous, or contradictory information, and defines Ask-F1 from question precision and blocker recall [@trinh2026hilbench]. In research workflows, the analogous task is to refuse an unsupported claim, preserve a failed run, or request a decision before a protocol violation becomes a result.

EviGateBench addresses this narrow systems question: can a reproducibility-oriented harness distinguish direct continuation, detection without containment, and gated containment on pre-specified research-workflow defects? Its contributions are a phase-gated artifact contract, a versioned synthetic task corpus with scorer-only keys, deterministic validators for provenance and overwrite protection, and a reference-controller study that validates behavioral separation.

## 2. Related Work and Scope

PaperBench demonstrates the scale and difficulty of end-to-end AI-research replication [@starace2025paperbench]. Its task and rubric design motivates preserving fine-grained audit records here, but EviGateBench is not numerically comparable because it uses fictional packets and scripted controllers rather than paper-scale replication tasks.

HiL-Bench provides a conceptual basis for escalation: a missing requirement should be surfaced rather than guessed [@trinh2026hilbench]. EviGateBench borrows this principle only for synthetic protocol blockers. It does not reuse HiL-Bench tasks, report Ask-F1, or claim cross-domain metric comparability.

AgentBench establishes that agent evaluation should include interaction, reasoning, and decision making [@liu2024agentbench]. EviGateBench narrows the target to evidence and provenance controls. The scope excludes real-paper writing quality, scientific novelty, human subjects, external tools, and LLM-generated code execution.

## 3. Benchmark and System Design

### 3.1 Artifact model

The EviGate workflow uses persistent files rather than chat memory as the scientific record. A verified source has a Source ID, stable locator, verification method, and support scope. A run manifest is created before execution and includes task ID, condition, seed, runtime, configuration, environment lock, commit, budget, stop condition, and output path. A writer cannot overwrite a raw output path. A manuscript claim must link to verified Source IDs and, for simulation-valued claims, to Run IDs.

### 3.2 Synthetic task corpus

The original v0.1 corpus contained 16 task packets across citation authenticity, claim support, run provenance, and escalation. A Phase-04 audit found that v0.1 exposed primary-defect and defect-token fields in agent-visible input. This was an answer-leakage defect, not a cosmetic issue. The corpus is preserved unchanged, documented as a negative result, and excluded from formal execution.

Version 0.2 retains 16 tasks in the same four families but removes answer-revealing fields from packets. Scorer-only answer keys specify the required flag and safe terminal action. The packets are fictional, contain no private data or full-text corpus, and test harness behavior rather than domain knowledge.

### 3.3 Conditions

Three deterministic reference controllers were implemented.

1. **Direct** always drafts and never flags a defect.
2. **Linear** applies fixed detection rules but always drafts after detection.
3. **EviGate** applies the same fixed detection rules, then blocks evidence or provenance defects and escalates protocol blockers.

The latter two controllers differ only in containment policy after detection. This makes the simulation useful for validating the scorer, while making it unsuitable for causal claims about a learned agent.

### 3.4 Outcomes and controls

Primary outcomes are detection, containment, and unsafe continuation. Detection requires the answer-key flag; containment requires blocking or escalating as appropriate; unsafe continuation records drafting despite the seeded issue. The v0.2 configuration registered 48 runs: 16 tasks multiplied by three conditions. Every run received a distinct manifest, fixed seed, configuration, environment lock, Git commit, budget, and output path before execution.

## 4. Deterministic Reference-Controller Study

### 4.1 Procedure

The formal study executed the 48 preregistered v0.2 manifests with the reference controller. Each raw record stores its manifest, controller submission, and deterministic score. Post-run validation confirmed that all 48 raw records were present, each score Run ID and task ID matched its manifest, and every manifest contained the required provenance fields. No raw record was retried, deleted, overwritten, or repaired.

### 4.2 Results

| Condition | Runs | Detection rate | Containment rate | Unsafe-continuation rate |
|---|---:|---:|---:|---:|
| Direct reference controller | 16 | 0.00 | 0.00 | 1.00 |
| Linear reference controller | 16 | 1.00 | 0.00 | 1.00 |
| EviGate reference controller | 16 | 1.00 | 1.00 | 0.00 |

The direct controller drafted through every packet. The linear controller detected every seeded issue but did not contain any because its policy always drafted. The EviGate controller detected every seeded issue and then applied its programmed block or escalation action. These results show that the scoring pipeline captures the intended distinction between detection and containment. They are deterministic consequences of the reference-controller rules, not a statistical estimate.

## 5. Discussion

The simulation illustrates two design points. Detection alone is insufficient for a research workflow: a controller may recognize a citation, provenance, or protocol problem and still produce an unsafe artifact. Containment is therefore a separate outcome.

The study also illustrates why failures must be preserved. The v0.1 answer leakage would have made a perfect detection score meaningless. Retaining the faulty corpus, recording the amendment, and executing only v0.2 makes the correction inspectable. This is more informative than silently replacing the test set.

The limits are equally important. The detector is scripted; it has no uncertainty calibration, language understanding beyond fixed rules, tool use, or independent judgment. The EviGate controller is designed to win the containment comparison. The results therefore cannot establish a performance advantage, causal mechanism, sample-based uncertainty estimate, or expected behavior for an LLM-based research agent. A credible subsequent study requires independent model rollouts, hidden answer keys, repeated seeds where randomness matters, blinded evaluation, and public task documentation.

## 6. Limitations

All tasks are synthetic and small. They do not represent the breadth of literature retrieval, coding, data licensing, statistical analysis, or scholarly writing. The controllers are deterministic reference implementations and must not be compared with PaperBench, HiL-Bench, AgentBench, or model leaderboards. The study has no independent seeds, LLM calls, human participants, or external judges, so statistical inference would be misleading. Finally, although v0.2 removes answer-revealing fields from packets, future evaluations must ensure that evaluated agents receive packets only and never answer-key paths or contents.

## 7. Conclusion

EviGateBench provides an evidence-gated research-workflow protocol with pre-run manifests, immutable outputs, source verification, claim mapping, and explicit failure preservation. A deterministic reference-controller simulation confirms that its scoring harness separates direct continuation, detection without containment, and gated containment on a corrected synthetic corpus. The strongest conclusion is narrow: the audited harness functions as specified for these scripted policies. Demonstrating reliable autonomous research behavior remains future work requiring independent agent evaluation.

## Data Availability

All fictional task packets, scorer-only answer keys, pre-run manifests, raw reference-controller records, analysis outputs, source records, and claim mappings are included in this repository. No private data, participant data, credentials, or restricted full text were used.

## Ethics Declaration

The study uses no human participants, animals, clinical data, or personal data. It does not execute LLM-generated code or interact with live journal, cloud, or production systems. The primary ethical risk is overclaiming simulated results; the protocol, analysis, and manuscript explicitly limit their interpretation.

## Author Contributions

Conceptualization, methodology, software, validation, and writing were completed by the EviGate project authors with AI assistance. A human author remains responsible for verification, authorship, and any submission decision.

## Conflict of Interest

The authors declare no known competing interests for this prototype study.

## Funding

No external funding supported this prototype study.

## AI Use Disclosure

AI assistance was used to design the benchmark protocol, implement the software, inspect artifacts, and draft this manuscript. All generated claims were constrained by versioned source records, raw artifacts, and the claim-evidence graph; a human author remains responsible for verification and any submission decision.

## References

- Liu, X., Yu, H., Zhang, H., et al. (2024). *AgentBench: Evaluating LLMs as Agents*. International Conference on Learning Representations. https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html
- Starace, G., Jaffe, O., Sherburn, D., et al. (2025). *PaperBench: Evaluating AI's Ability to Replicate AI Research*. arXiv:2504.01848. https://arxiv.org/abs/2504.01848
- Trinh, T., Elfeki, M., Luo, G., et al. (2026). *HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?* arXiv:2604.09408. https://arxiv.org/abs/2604.09408

## Claim–Evidence Index

| Manuscript claim | Claim ID | Evidence |
|---|---|---|
| PaperBench task and rubric framing | CLM-001 | SRC-PAPERBENCH-2025 |
| HiL-Bench Ask-F1 definition | CLM-002 | SRC-HILBENCH-2026 |
| AgentBench eight-environment framing | CLM-003 | SRC-AGENTBENCH-2024 |
| EviGate simulated condition result | CLM-004 | SRC-EVIGATE-SIM-V02; 16 EviGate Run IDs |
| Direct simulated condition result | CLM-005 | SRC-EVIGATE-SIM-V02; 16 Direct Run IDs |
| Linear simulated condition result | CLM-006 | SRC-EVIGATE-SIM-V02; 16 Linear Run IDs |

