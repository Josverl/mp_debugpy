#!/bin/bash
# Setup script after cloning

# Initialize and update direct submodules
git submodule update --init 

# Update to latest commits on tracked branches
git submodule update --remote

# Set up sparse checkout for micropython-lib
cd micropython-lib
git sparse-checkout init --cone
git sparse-checkout set python-ecosys/debugpy
git sparse-checkout reapply
cd ..

echo "Submodules initialized and updated!"
