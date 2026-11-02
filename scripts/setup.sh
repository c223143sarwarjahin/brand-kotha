#!/usr/bin/env bash
set -e

echo "========================================================================"
echo " BrandKotha Developer Environment Bootstrap"
echo "========================================================================"

# 1. Environment template check
if [ ! -f .env ]; then
  echo "--> Creating .env from .env.example..."
  cp .env.example .env
fi

# 2. Python Virtual Environment Check
if [ ! -d "apps/api/.venv" ]; then
  echo "--> Creating Python virtual environment in apps/api/.venv..."
  python3 -m venv apps/api/.venv
fi

echo "--> Installing Python dependencies..."
source apps/api/.venv/bin/activate
pip install --upgrade pip
pip install -r apps/api/requirements.txt
deactivate

# 3. Node / pnpm Dependencies Check
echo "--> Installing pnpm workspace packages..."
pnpm install

echo "========================================================================"
echo " Setup complete! Run 'make dev' to start the full stack."
echo "========================================================================"
