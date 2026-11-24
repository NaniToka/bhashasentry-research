#!/bin/bash
set -e
echo "Packaging BhashaSentry release artifacts..."
tar -czf bhashasentry_v0.1.0_artifacts.tar.gz src experiments data docs
echo "Package bhashasentry_v0.1.0_artifacts.tar.gz created."
