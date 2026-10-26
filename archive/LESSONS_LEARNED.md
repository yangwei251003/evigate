# EviGateBench lessons learned

1. **Answer-key separation is a validity requirement.** The original v0.1
   corpus leaked defect information into visible packets. Preserving that
   failure and creating v0.2 was necessary before formal execution.
2. **Detection and containment are different behaviors.** The linear reference
   controller detected all seeded issues while still drafting through every
   one; a benchmark that records detection alone would miss that failure.
3. **A reproducible harness is not an empirical agent study.** Scripted
   controllers are useful for testing provenance and scoring pathways, but they
   cannot establish LLM-agent effectiveness or scientific reliability.
4. **Immutable manifests make audit possible.** The 48 formal outputs can be
   traced to configuration, seed, environment lock, commit, and raw record.
5. **Future work needs independent evaluation.** A submission-grade extension
   requires answer-key isolation, independent model rollouts, repeated seeds,
   blinded assessment, and a broader task suite.
