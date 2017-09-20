# File: ODBC.pl
# Purpose: Provide code to interface with a database via ODBC.
# Author: James Heydorn
use DBI;

# Sub: RunSQL
# Purpose: Run an SQL statement and return any data from it.
# Parameters:
# 	$_[0] : the ODBC system data source to use
# 	$_[1] : the SQL statement to run
# 	$_[2] : A reference variable to the array that will receive the data, (optional, set to zero if the next parameter is used and you don't want this array)
# 	$_[3] : The name of an output file (optional)
# Example call: RunSQL($DSN,$SQL,*SQLData)
# Output:
# The reference variable becomes an array with two indexes.  The first index references the row of data and
# the second index references the column or field within the row. The first row is populated with the field names.
# To access individual elements you can use these syntaxes:
# 
# To access a specific field value for a specific record:
# $value=$SQLData[row][col];
# 
# To simply list all the query return values, one per line:
# for ($i=0;$i<=$#SQLData;$i++) {
# 	@items=@{$SQLData[$i]}; # This gets the row into @items.
# 	foreach $item (@items) { print "Record $i: $item\n"; }}
#
# To process each record individually using a hash:
# @fieldnames=@{$SQLData[0]};
# for ($i=1;$i<=$#SQLData;$i++) {
# 	@values=@{$SQLData[$i]}; # This gets the row into @values.
# 	for ($j=0;$j<=$#values;$j++) { $record{$fieldnames[$j]}=$values[$j]; }
# 	# Now the %records hash has keys of column names and values of their corresponding values.
# 	print "Record $i:\n";
# 	foreach $key (keys(%record)) { print "$key = $record{$key}\n"; }}
#
# See perllol in the Perl documentation for more details on how to access elements in multidimensional arrays.
sub RunSQL {
	my ($i,$j);

	# Parameters
	my $MaxFieldSize=65536;

	# Get arguments.
	my $DSN=$_[0];
	if (!DSN) { print 'Missing data source'; exit; }
	$DSN="dbi:ODBC:$DSN";
	my $sql=$_[1];
	if (!$sql) { print 'Missing SQL statement'; exit; }
	local *data=$_[2] if $_[2];
	my $OutFile=$_[3] if $_[3];

	# Open a connection.
	my $dbh=DBI->connect($DSN,'','',{ RaiseError=>1,PrintError=>0,AutoCommit=>1 });
	if (!defined($dbh)) { print "Unable to connect to $DSN"; exit; }
	$dbh->{odbc_exec_direct}=1; # Patch to avoid invalid cursor state errors for some SQL statements for MS SQL Server
	$dbh->{LongReadLen}=$MaxFieldSize; # This only applies to SELECT statements. It is needed to prevent the driver from bombing on long data.

	# Run the SQL.
	my $sth=$dbh->prepare($sql);
	my $rv=$sth->execute;
	if (!$rv) { $dbh->disconnect; exit; }

	# Deal with the returned SQL data, if applicable.
	if (!$_[2] && !$OutFile) { $sth->finish; $dbh->disconnect; return; }
	my @fields=@{$sth->{NAME}};
	if ($#fields<0) { print 'No field names found'; exit; }
	if ($_[2]) {
		for ($j=0;$j<=$#fields;$j++) { $data[0][$j]=$fields[$j]; }
		$i=1; }
	if ($OutFile) {
		if (!open(RUNSQLOUTF,">$OutFile")) { print "Unable to write $OutFile: $!"; exit; }
		for ($j=0;$j<=$#fields;$j++) { print RUNSQLOUTF "$fields[$j]"; print RUNSQLOUTF "\t" if $j<$#fields; }
		print RUNSQLOUTF "\n"; }
	while (my %row=%{$sth->fetchrow_hashref}) {
		if ($_[2]) { for($j=0;$j<=$#fields;$j++) { $data[$i][$j]=$row{$fields[$j]}; }}
		if ($OutFile) {
			for($j=0;$j<=$#fields;$j++) { print RUNSQLOUTF "$row{$fields[$j]}"; print RUNSQLOUTF "\t" if $j<$#fields; }
			print RUNSQLOUTF "\n"; }
		$i++ if $_[2]; }
	close(RUNSQLOUTF) if $OutFile;

	# Close the connection.
	$dbh->disconnect; }
1;