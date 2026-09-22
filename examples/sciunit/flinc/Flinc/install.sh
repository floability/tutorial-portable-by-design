#!/bin/bash
set -e

if (( $# != 1 ))
then
  echo "Provide the user kernel path as an argument!"
  exit 1
fi

# --- config for the on-the-fly sciunit build -------------------------------
SCIUNIT_REPO_URL="https://github.com/radiant-systems-lab/sciunit.git"
SCIUNIT_REF="master"    # branch or tag to build from
PATCH_DIR="$(pwd)/patches"

if ! command -v git &> /dev/null
then
    apt-get update
    apt-get install -y git
fi

# step 1: download sciunit from upstream, apply FLINC's changes by content
# match (patches/apply_patches.py -- robust to upstream formatting changes,
# unlike a byte-exact .patch file), and build + install it from source
# (replaces the old bundled .tar.gz). cmake itself is fetched automatically
# via setup_requires, so no root/apt-get is needed for it.

BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "${BUILD_DIR}"' EXIT

git clone --branch "${SCIUNIT_REF}" "${SCIUNIT_REPO_URL}" "${BUILD_DIR}/sciunit"

python3 "${PATCH_DIR}/apply_patches.py" "${BUILD_DIR}/sciunit"

pushd "${BUILD_DIR}/sciunit" > /dev/null

pip install .

popd > /dev/null

sciunit create -f audit-kernel

# step 2: copy kernel.json file of user kernel
kernelfilepath="$1/kernel.json"
auditkerneldir="audit-kernel"
mkdir -p ${auditkerneldir}
cp ${kernelfilepath} ${auditkerneldir}

# step 3: add script instructions
auditkernelpath="audit-kernel/kernel.json"
add="\\\t\"$(pwd)/handler.py\",\"sciunit\",\"exec\","
# sed -i "/prepend_and_launch.sh\",/a $add" ${auditkernelpath}
sed -i "/argv\": \[/a $add" ${auditkernelpath}

if ! command -v python &> /dev/null
then
    apt-get update
    apt-get install -y python-is-python3
fi

# step 4: update kernel name
sed -i -E "s/(\"display_name\": \")(.+)\",/\1Sciunit Audit(\2)\",/" ${auditkernelpath}

# step 5: install the audit kernel
jupyter kernelspec install --sys-prefix audit-kernel/
echo "Installed the audit kernel"

# # step 6: update the repeat kernel
# repeatkernelpath="repeat-kernel/kernel.json"
# add="\\\t\"$(pwd)/repeat-handler.py\","
# sed -i "/argv\": \[/a $add" ${repeatkernelpath}

# step 7: cp repeat handler to sciunit folder to be used in repeat kernel generation
cp repeat-handler.py ~/sciunit/


# step 8: install the repeat kernel
jupyter kernelspec install --sys-prefix repeat-kernel/
echo "Installed the repeat kernel"

# now just execute the notebook code with the audit and repeat kernels