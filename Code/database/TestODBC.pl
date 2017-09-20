require 'ODBC.pl';

# Test parameters
$DSN='Photos';
$sql="SELECT * FROM frames WHERE mission='ISS048' AND roll='E' AND frame='    338  '";

RunSQL($DSN,$sql,*SQLData);
@fieldnames=@{$SQLData[0]};
print 'Field names returned: ';
foreach (@fieldnames) { print "$_ "; }
print "\n";
for ($i=1;$i<=$#SQLData;$i++) {
	@values=@{$SQLData[$i]}; # This gets the row into @values.
	for ($j=0;$j<=$#values;$j++) { $record{$fieldnames[$j]}=$values[$j]; }
	# Now the %records hash has keys of column names and values of their corresponding values.
	print "Record $i:\n";
	foreach $key (keys(%record)) { print "$key = \"$record{$key}\"\n"; }}
