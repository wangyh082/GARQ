#!/usr/bin/env bash
set -u

gpu="$1"
shift
mkdir -p revision_results/phase2/logs
for config in "$@"; do
  stem="$(basename "$config" .yaml)"
  log="revision_results/phase2/logs/${stem}.driver.log"
  status="revision_results/phase2/logs/${stem}.status"
  CUDA_VISIBLE_DEVICES="$gpu" /usr/bin/time -v \
    /home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.run --config "$config" \
    >"$log" 2>&1
  code=$?
  printf '%s\n' "$code" >"$status"
done
