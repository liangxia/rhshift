#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

for file in $(ls $SCRIPT_DIR) ; do
	if [[ -L $file ]] ; then
		IFS='#' read script_file home dpath <<< $file
		workdir="$HOME/${dpath//#//}"
		if [[ -f $script_file ]] && [[ -d $workdir ]] ; then
			pushd "$workdir" &> /dev/null
			if ! [[ -e "$workdir/$script_file" ]] ; then
				echo "Link from '$SCRIPT_DIR/$script_file' to '$workdir/$script_file'"
			        ln -s "$SCRIPT_DIR/$script_file" "$script_file"
			fi
			popd &> /dev/null
		fi
	fi
done
