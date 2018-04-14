#!/bin/bash    

# the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# the temp directory used, within $DIR
# omit the -p parameter to create a temporal directory in the default location
WORK_DIR=`mktemp -d -p "$DIR"`

# check if tmp dir was created
if [[ ! "$WORK_DIR" || ! -d "$WORK_DIR" ]]; then
  echo "Could not create temp dir"
  exit 1
fi

# deletes the temp directory
function cleanup {      
  rm -rf "$WORK_DIR"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

python -m grpc_tools.protoc -I proto --python_out=$WORK_DIR --grpc_python_out=$WORK_DIR `ls $DIR/proto`
GENERATED_FILES=`ls -C $WORK_DIR`
mv $WORK_DIR/* $DIR/
2to3 -n -w --no-diffs $GENERATED_FILES 2>/dev/null

echo "Generated python files successfully"
