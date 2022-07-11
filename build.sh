#!/bin/sh

if [ $# -ne 1 ]; then
    echo "./build.sh version"
    exit 1
fi

rm -rf screeps.docset screeps.tgz

cp -r screeps.docset-tmpl/ screeps.docset
sed -i "" -e "s/_VERSION_/$1/g" screeps.docset/Contents/Info.plist
cp -r Documents/$1 screeps.docset/Contents/Resources/Documents/
./gen.py $1
mv docSet.dsidx screeps.docset/Contents/Resources/

tar zcf screeps.tgz screeps.docset
