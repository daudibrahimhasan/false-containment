# False Containment Experiment

This project measures when an incident-response system declares an incident resolved even though manually defined, model-independent ground truth says it is unresolved.

## Core design

- Ground truth is written by the experiment author in each incident JSON file. Agents and verifiers cannot change it.
- Evidence conditions are specific to an incident, while `taxonomy_tags` map them to shared categories for cross-incident analysis.
- A false containment is a verifier verdict of `resolved` when ground truth is `unresolved`.
- False Containment Rate (FCR) is `false_containments / all_resolved_verdicts`. The output also includes the unconditional false-containment frequency so the denominator is never ambiguous.
- The final matrix is 20 incidents x 2 agent models x 5 evidence conditions x 10 replicates = 2,000 verifier runs.

`NVIDIA: Nemotron 3 Embed 1B (free)` is an embedding model. It cannot generate incident-response trajectories or verifier judgments, so it is intentionally not used as an agent or verifier model. Actual generative OpenRouter model IDs remain unset in `config/experiment.json`.

## Run the included offline test

No API key or third-party package is needed:

```powershell
python -m false_containment.cli run --mock
```

If the package has not been installed, use:

```powershell
$env:PYTHONPATH="src"
python -m false_containment.cli run --mock
```

The mock run executes one synthetic SSH incident with two deterministic mock agents, five conditions, and ten replicates, for 100 verifier runs. It writes raw trajectories, evidence packets, verdicts, copied ground truth, CSV/JSON results, an SVG plot, and Markdown/CSV tables under `outputs/`.

## Run with OpenRouter later

1. Put the key after `OPENROUTER_API_KEY=` in `.env`.
2. Replace the empty model lists/values in `config/experiment.json` with two generative agent model IDs and one generative verifier model ID.
3. Run `python -m false_containment.cli run`.

The online provider uses OpenRouter's OpenAI-compatible chat completions endpoint. Model responses must be JSON. A failed or malformed response is saved as a run error and is never silently converted into a verdict.

## Add the remaining incidents

Copy the schema in `incidents/ssh_unauthorized_key.json`. Each incident needs exactly five evidence conditions and a manually authored `ground_truth.status`. Once there are 20 valid incident files, the configured matrix produces 2,000 runs automatically.
