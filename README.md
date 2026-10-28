# ghostline

A tiny code séance for **Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine**. Give it a deleted file in a Git repository. It retrieves the file's last surviving version and deletion commit, then asks an open-weight model to write a short first-person testimony. Every response must cite real evidence IDs; an invented citation makes the run fail.

This is a new project created during the October 26–31, 2026 challenge window. MIT licensed. Python 3.10+, Git, and no Python package dependencies.

## Reproduce the demo

The demo history is **fictional and generated locally**. It is not presented as a production incident.

[Watch the captured 15-second demo](https://github.com/build996/ghostline/releases/download/v0.1.0/ghostline-demo.mp4). The video is rendered from an actual model run saved in [`demo/captured-run.txt`](demo/captured-run.txt). It shows a mistake the model made about the cache write and the source lines that disprove it.

```bash
python demo/make_history.py demo-history
python ghostline.py demo-history --file legacy_cache.py --evidence-only
export NVIDIA_API_KEY=...  # PowerShell: $env:NVIDIA_API_KEY="..."
python ghostline.py demo-history --file legacy_cache.py
python -m unittest discover -s tests -v
```

The default model is [NVIDIA Nemotron 3.5 Lightning 30B A3B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16), called through NVIDIA's hosted API. The model and endpoint can be replaced with `--model` and `--endpoint` if your server speaks the same chat completions format. The demo is **not offline**. The open weights make self-hosting possible, subject to hardware and model licensing.

## How it works

1. Git identifies the most recent commit that deleted the requested path.
2. `git show PARENT:path` recovers the last surviving source. The CLI groups numbered source lines into small `S1`, `S2`, etc. evidence blocks, and labels commit metadata `C1` and `C2`.
3. The model writes a compact "ghost" account and selects 2–5 evidence IDs. The CLI rejects IDs absent from the source bundle.
4. The output prints the exact cited lines and a separate uncertainty sentence.

This does not prove the model's prose is true. A model can make an unsupported claim while citing a real line. Review the source before relying on the interpretation. The tool sends source excerpts to the configured model endpoint and redacts common credential patterns only on a best-effort basis; use `--evidence-only` or a self-hosted endpoint for sensitive repositories. It reads at most 80 source lines, so it can miss context from larger files.
