set -e 
TMP_TXT="mem_check_all.txt"
echo "\n---\nVALGRIND SUMMARY:"
passing="$(grep "All heap blocks were freed -- no leaks are possible" ${TMP_TXT}| wc -l)"
total="$(grep "Memcheck, a memory error detector" ${TMP_TXT} | wc -l)"
echo "${passing} of ${total} mem tests passing"
echo "---\n"
