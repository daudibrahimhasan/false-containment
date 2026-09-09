# Operational Amendment: Preregistration v1.5.2

Date: 2026-09-09

The first v1.5.1 GLM pilot attempt stopped before completing a trajectory because the provider returned a non-text `message.content` value. The runner raised an unhandled parser exception and wrote no trajectory or evidence packet. No verifier call occurred and no scientific result was created.

Version 1.5.2 makes only the surgical operational correction required by the frozen failure policy: non-text or otherwise malformed provider content is handled as a failed request, retried under the existing fixed policy, and recorded as infrastructure/pending if retries are exhausted. It does not parse hidden reasoning content, change the prompt, alter simulator semantics, change models, or substitute another provider.

The fresh GLM-5.3/Gemini pilot must run from the empty v1.5.2 output directory. DeepSeek trajectories are not reused. Qwen and Nemotron remain uncalled.
