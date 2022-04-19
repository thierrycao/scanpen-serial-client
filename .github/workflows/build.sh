##########################################################################
# File Name: build.sh
# Author: ThierryCao
# mail: iamthinker@163.com
# Created Time: 六 11/ 6 17:52:57 2021
#########################################################################
#!/bin/bash
git push origin :refs/tags/v1.0.0
git tag -d v1.0.0
git tag -a v1.0.0 -m "v1.0.0"
git push --tags
