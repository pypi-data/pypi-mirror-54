#!/bin/sh
###################################################
# PyNonameDomain helper script for using lego     #
#    Part of the PyNonameDomain package           #
#                                                 #
#        Copyright (C) 2019  Erovia               #
#                                                 #
# This program comes with ABSOLUTELY NO WARRANTY. #
# This is free software, and you are welcome      #
# to redistribute it under certain conditions.    #
#                                                 #
###################################################

# Set your API username and password below #
if [ -z $NND_USERNAME ]; then
	export NND_USERNAME=""
fi
if [ -z $NND_PASSWORD ]; then
	export NND_PASSWORD=""
fi

####### DO NOT CHANGE BELOW THIS LINE #######
export NND_DOMAIN="$2"
export CERTBOT_VALIDATION="$3"
if [ -z $NND_USERNAME ] || [ -z $NND_PASSWORD ]; then
	echo "Please provide username and password."
	exit 2
fi
export NND_TOKEN="$(nnd-cli login -q)"
if [ -z $NND_TOKEN ]; then
	echo "Could not get API token. Check login details."
	exit 3
fi

if [ $1 == "present" ]; then
	nnd-cli create -c
elif [ $1 == "cleanup" ]; then
	HASH=$(nnd-cli read -q -r "{\"text\":\"$CERTBOT_VALIDATION\"}")
	nnd-cli remove -q --hash $HASH
else
	exit 1
fi
