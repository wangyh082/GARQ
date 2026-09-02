#!/usr/bin/env bash
set -u

dataset="$1"
gpu="$2"
log_root="revision_results/phase2/logs"
mkdir -p "$log_root"

for batch in 512 1024 2048; do
  for seed in 0 1 2; do
    name="P2_E8_${dataset}_batch${batch}_seed${seed}"
    config="revision_exp/configs/batch_size_full/p2_${dataset}_batch${batch}_seed${seed}.yaml"
    CUDA_VISIBLE_DEVICES="$gpu" /usr/bin/time -v \
      /home/zhangpeiru/.conda/envs/MetqQ2/bin/python -m revision_exp.run --config "$config" \
      > "$log_root/${name}.driver.log" 2>&1
    status=$?
    printf '%s\n' "$status" > "$log_root/${name}.status"
    if [[ "$status" -ne 0 ]]; then
      printf '%s\n' "FAIL $name; continuing queue with preserved evidence"
    else
      printf '%s\n' "PASS $name"
    fi
  done
done
