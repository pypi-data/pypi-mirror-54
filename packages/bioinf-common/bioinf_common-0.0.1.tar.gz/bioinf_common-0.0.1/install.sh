cd "$( dirname "${BASH_SOURCE[0]}" )"

rm -rf ./build/ # enforce recompilation

pip3 install \
    --user -U \
    -e .

#--verbose \
#--global-option=build_ext --global-option="-I/usr/local/include" \
