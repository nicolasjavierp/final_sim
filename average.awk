BEGIN{FS=",";count=0;}
{
$1=substr($1,2)+0;
$NF=substr($NF,1,length($NF)-1);
for (i=1;i<=NF;i++) v[i]+=$i;
count++;
}
END{
	#print "Archivos procesados: ", count;
	for (i=1;i<=NF;i++) printf "%g\t", v[i]/count;
	print "";
}
