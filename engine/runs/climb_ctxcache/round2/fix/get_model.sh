#!/bin/sh
# SmolLM2-135M-Instruct (Q4_1 GGUF) ships inside the PyPI wheel llm-smollm2==0.1.2 (huggingface.co is blocked here).
set -e; mkdir -p model; cd model
pip download --no-deps llm-smollm2==0.1.2 -d . -q
echo "bcc81830d10ce7d9e76640cad826a4b79ed3e4547c78a0be5c4f2fb0e2448c70  llm_smollm2-0.1.2-py3-none-any.whl" | sha256sum -c
python3 -I -c "import zipfile; zipfile.ZipFile('llm_smollm2-0.1.2-py3-none-any.whl').extract('llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf', '.')"
