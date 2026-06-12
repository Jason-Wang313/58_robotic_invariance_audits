import csv, os, json
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docs")
CSV_PATH = os.path.join(DOCS, "related_work_matrix.csv")

def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    rows = load_rows()
    top300 = rows[:300]
    hostile100 = rows[:100]
    # Simple topical buckets
    buckets = defaultdict(list)
    for r in top300:
        title = r["title"].lower()
        if "equivari" in title or "invari" in title:
            buckets["invariance"].append(r)
        elif "world model" in title:
            buckets["world_models"].append(r)
        elif "sim" in title and "real" in title:
            buckets["sim2real"].append(r)
        elif "tactile" in title or "proprio" in title:
            buckets["sensing"].append(r)
        elif "manip" in title or "control" in title or "policy" in title:
            buckets["control"].append(r)
        else:
            buckets["general"].append(r)

    lit = []
    lit.append("# Literature Map")
    lit.append("")
    lit.append("This map is a first-pass, evidence-light organization of the 1000+ paper sweep into the themes that matter for a robotic invariance audit thesis.")
    lit.append("")
    lit.append("## Core direction candidate")
    lit.append("")
    lit.append("Audit whether robot models are actually invariant to embodied transformations they claim to handle, and separate true symmetry preservation from benchmark-specific robustness.")
    lit.append("")
    lit.append("## Theme buckets")
    for name in ["invariance", "world_models", "sim2real", "sensing", "control", "general"]:
        lit.append(f"### {name}")
        for r in buckets.get(name, [])[:12]:
            lit.append(f"- {r['title']} ({r['year']})")
        lit.append("")
    write(os.path.join(DOCS, "literature_map.md"), "\n".join(lit))

    hostile = []
    hostile.append("# Hostile Prior Work")
    hostile.append("")
    hostile.append("These are the papers most likely to weaken a claim that invariance auditing is a new central mechanism. Many are close neighbors rather than exact duplicates, so the burden is to show the gap precisely.")
    hostile.append("")
    for r in hostile100:
        hostile.append(f"- {r['title']} ({r['year']})")
    write(os.path.join(DOCS, "hostile_prior_work.md"), "\n".join(hostile))

    nb = []
    nb.append("# Novelty Boundary Map")
    nb.append("")
    nb.append("## Hidden assumptions we can attack")
    assumptions = [
        "The robot model preserves symmetry because the architecture is designed to be equivariant.",
        "Benchmark gains imply actual invariance under real embodied transformations.",
        "Viewpoint changes are representative of all relevant robot transformations.",
        "A model's performance under distribution shift implies preserved internal geometry.",
        "External calibration fixes are enough to certify invariance.",
        "One can infer invariance from success rates alone.",
        "Symmetry only matters at the perception layer, not at action selection or memory.",
        "Known SE(3) symmetry is the only important symmetry in robotics.",
        "Data augmentation and equivariance are interchangeable in practice.",
        "Invariant representations remain invariant after closed-loop rollouts.",
        "Cross-embodiment transfer is a proxy for invariance preservation.",
        "World models inherit invariances from their encoders.",
        "Contact, friction, and actuation errors are nuisance variables rather than core symmetry breakers.",
        "A model can be invariant on average without being invariant per task state.",
        "Hardware and camera perturbations are separable from policy invariance.",
        "Observed robustness is not just learned coverage of common nuisance distributions.",
        "Latent consistency implies causal consistency.",
        "Benchmark transformations are faithful to embodied transformations.",
        "Symmetry-preserving modules can be layered without changing downstream behavior.",
        "A failure to generalize means a failure of invariance, not of supervision or optimization."
    ]
    for a in assumptions:
        nb.append(f"- {a}")
    nb.append("")
    nb.append("## Candidate directions")
    dirs = [
        "Auditing invariance as a property of the full robot pipeline: perception, latent state, policy, and closed-loop rollout.",
        "Constructing counterfactual embodied transformations that preserve task semantics but break naive visual similarity.",
        "Comparing architecture-level equivariance with empirical invariance under perturbations that only appear at execution time.",
        "Separating invariance to camera pose from invariance to contact, embodiment, and dynamics changes.",
        "Treating invariance as a measurable claim with falsification tests rather than a design slogan."
    ]
    for d in dirs:
        nb.append(f"- {d}")
    write(os.path.join(DOCS, "novelty_boundary_map.md"), "\n".join(nb))

    nd = """# Novelty Decision

Chosen thesis: robot models often advertise invariance or symmetry preservation, but the invariance usually exists only at the easiest observable layer; an audit that intervenes on embodied transformations can expose where invariance collapses across perception, memory, and control.

Why this is the strongest direction:
- It changes the central mechanism from building another symmetric model to measuring whether claimed symmetry is real.
- It directly attacks a field assumption: benchmark robustness is taken as evidence of invariance.
- It is compatible with a runnable audit framework and does not require inventing a bigger model or new benchmark as the main contribution.

Rejected alternatives:
- New equivariant architecture: too close to existing literature.
- Pure benchmark proposal: weak unless the audit mechanism is the contribution.
- Uncertainty/verification add-ons: do not change the central mechanism enough.
"""
    write(os.path.join(DOCS, "novelty_decision.md"), nd)

    claims = """# Claims

1. Many robot papers conflate robustness under nuisance shifts with true invariance under embodied transformations.
2. The strongest novelty is an audit protocol that probes invariance at multiple pipeline stages.
3. Viewpoint-only tests are insufficient because contact, kinematics, and execution-time perturbations can destroy invariance after the encoder.
4. A falsification-oriented audit can reveal that some reported symmetry preservation is architectural, while some is merely dataset coverage.
5. The paper should avoid claiming universal proofs unless the test suite explicitly spans the relevant transformation family.
"""
    write(os.path.join(DOCS, "claims.md"), claims)

    attacks = """# Reviewer Attacks

- "This is just robustness evaluation with a new name."
- "The audit is benchmark-specific and does not prove anything about invariance in general."
- "Equivariance methods have already been analyzed extensively; the paper does not add a new mechanism."
- "If the audit depends on handcrafted transformations, it may miss latent symmetry failures."
- "The claims about closed-loop behavior may not transfer across embodiments."
- "Any positive results could simply reflect better data coverage."
"""
    write(os.path.join(DOCS, "reviewer_attacks.md"), attacks)

    with open(os.path.join(DOCS, "analysis_summary.json"), "w", encoding="utf-8") as f:
        json.dump({
            "top300": len(top300),
            "hostile100": len(hostile100),
            "themes": {k: len(v) for k, v in buckets.items()},
        }, f, indent=2)

if __name__ == "__main__":
    main()
