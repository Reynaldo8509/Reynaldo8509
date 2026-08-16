# Repository synchronization

The canonical public repository for this project is
[`Reynaldo8509/Reynaldo8509`](https://github.com/Reynaldo8509/Reynaldo8509),
where the HomeLab lives at `projects/soc-operations-lab/`. The former standalone
`soc-operations-lab` repository was consolidated into that portfolio repository.

## Safe local workflow

Clone or update the canonical repository, then work inside the project subtree:

```bash
git clone https://github.com/Reynaldo8509/Reynaldo8509.git "$HOME/Reynaldo8509"
git -C "$HOME/Reynaldo8509" pull --ff-only origin main
cd "$HOME/Reynaldo8509/projects/soc-operations-lab"
```

Before an integration, preserve a bundle and a working-tree archive of any legacy
checkout. Do not force-push a legacy standalone history over the portfolio
repository: the two histories are intentionally independent after consolidation.

## Integration policy

- The cloud copy is authoritative for files already present in the project subtree.
- New local evidence is imported only after secret/PII and link checks pass.
- A recovery branch and pull request keep each integration reviewable and reversible.
