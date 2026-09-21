conda create --name sciunit-env --clone portable-by-design -y
conda install --name sciunit-env langchain=1.0.3 langchain-community=0.3.31 langchain-text-splitters=0.3.11 rank-bm25=0.2.2 -y
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sciunit-env