for n in {12..28}
do
 ../../scripts/waveform.py ALL00${n}/A00${n}CH1.CSV ALL00${n}/A00${n}CH2.CSV ../A00${n}.pdf
done
