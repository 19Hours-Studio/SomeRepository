#!/bin/sh
# Qwen3-0.6B from Docker Hub's model-artifact registry (ai/qwen3:0.6b-safetensors); verifies each blob digest.
set -e
D=${QWEN_DIR:-/tmp/claude-0/w/qwen3}; R=ai/qwen3; mkdir -p "$D"; cd "$D"
T=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$R:pull" | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
curl -s -H "Authorization: Bearer $T" -H "Accept: application/vnd.oci.image.manifest.v1+json" \
  https://registry-1.docker.io/v2/$R/manifests/0.6b-safetensors > manifest.json
python3 -c "
import json
for l in json.load(open('manifest.json'))['layers']: print(l['digest'], l['annotations']['org.cncf.model.filepath'])" |
while read d f; do
  curl -sL -H "Authorization: Bearer $T" -o "$f" https://registry-1.docker.io/v2/$R/blobs/$d
  [ "sha256:$(sha256sum "$f" | cut -d' ' -f1)" = "$d" ] && echo "ok $f" || { echo "DIGEST MISMATCH $f"; exit 1; }
done
