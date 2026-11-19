#!/bin/bash
cd /home/user/videos-ai/video/ep106
./make_variant.sh "I built an app in half an hour." V1 "AN APP|IN HALF|AN HOUR" 2 > out/make-V1.log 2>&1
./make_variant.sh "Eleven free add-ons. One app, built by Claude." V2 "11 FREE|ADD-ONS|ONE APP" 2 > out/make-V2.log 2>&1
./make_variant.sh "Claude found problems in my app idea." V3 "PROBLEMS|IN MY|APP IDEA" 0 > out/make-V3.log 2>&1
./make_variant.sh "App idea? Give it to Claude." V4 "APP IDEA?|GIVE IT|TO CLAUDE" 2 > out/make-V4.log 2>&1
./make_variant.sh "This free Claude tool plans and builds apps." V5 "FREE|CLAUDE TOOL|BUILDS APPS" 2 > out/make-V5.log 2>&1
echo ALLDONE > out/runall.done
