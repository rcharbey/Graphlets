classe='4'
to_read='../Results/facebook_k5/Typo_5/egos_classe_'$classe'.csv'
mkdir '/home/raphael/Project_Motifs/Results/facebook_k5/Typo_5/Visu/Typo_'$classe
for ego in `cat $to_read`
do
	cp '/home/raphael/Graphs/visu/'$ego'.svg' '/home/raphael/Project_Motifs/Results/facebook_k5/Typo_5/Visu/Typo_'$classe'/'$ego'.svg'
done
