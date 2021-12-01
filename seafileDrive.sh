export PATH=/opt/homebrew/bin:$PATH
for f in "$@"
do
	dest=""
	if [[ $f == * ]]
	then
		filename=$(exiftool -T $f -DateTimeOriginal | awk '{print $1;}')
		# Change destination local folder path
		dest="/Users/bigpapa/Documents/GoogleDriveSync/$filename" && mkdir $dest
	fi
	if [[	$dest != "" ]]
	then
	cp $f $dest 
	fi
done