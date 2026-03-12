#!/bin/bash
repo=$1

echo "Scanning repository..."

tree -L 3 $repo > repo_tree.txt
cloc $repo > repo_metrics.txt

echo "scan_complete"
