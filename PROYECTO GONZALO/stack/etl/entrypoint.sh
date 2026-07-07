#!/bin/bash
set -e

echo "=== JOB 1: carga inicial ==="
python primera_carga.py

echo "=== JOB 2: carga continuada (loop infinito) ==="
exec python carga_continuada.py
