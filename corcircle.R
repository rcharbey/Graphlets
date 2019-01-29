library(ade4)
library(cluster)
library(fpc)

file_name <- 'representativity_taille.csv'
size_min <- 0
size_max <- 5000
all_motifs <- TRUE

in_range <- function(x, r1, r2){
	return ((x >= r1) & (x <= r2))
}

donnees <- read.csv(file_name, header = TRUE, sep = ";")

donnees_matrix <- as.matrix(donnees)

nb_concerned_ego <- 0
for (i in 1:nrow(donnees_matrix)){
	enum <- matrix(donnees_matrix[i,])
	if (in_range(enum[1], size_min, size_max)){
		nb_concerned_ego <- nb_concerned_ego + 1
	}
}

if (all_motifs == FALSE){
	nb_col <- 21
	range_label <- 10:30
} else {
	if (grepl('repr', file_name)){
		nb_col <- 29
		range_label <- 2:30
	} else {
		nb_col <- 30
		range_label <- 1:30
	}
}

mat_donnees <- matrix(data=NA, nrow = nb_concerned_ego, ncol=nb_col)

j <- 0
for (i in 1:nrow(donnees_matrix)){
	enum <- matrix(donnees_matrix[i,])
	if (in_range(enum[1], size_min, size_max)){
		if (grepl('repr', file_name)){
			if (all_motifs == TRUE){
				to_add <- enum[c(seq(2,30)),]
			} else {
				to_add <- enum[c(seq(10,30)),]
			}
		} else {
			if (all_motifs == TRUE){
				to_add <- enum[c(seq(3,31)),]
			} else {
				to_add <- enum[c(seq(11,31)),]
			}
		}
		print(to_add)
		print(length(to_add))
		print(length(mat_donnees[1,]))
		j <- j + 1
		mat_donnees[j, ] <- to_add
	}
}


dudi1 <- dudi.pca(mat_donnees, scan = FALSE, nf = 3) # a normed PCA
data <- dudi1$tab

## Sommes cumulées des contributions
kip <- 100 * dudi1$eig/sum(dudi1$eig)
cumsum(kip)

## Choix des composantes pour les cercles de correlations
dudi1$c1
l <- list(dudi1$c1[2], dudi1$c1[3])

## Cercles de correlations
s.corcircle(l, label = range_label)

##kmeans
cl <- kmeans(data, 4)
plotcluster(data, cl$cluster, pch = 16)

##centres
cl$centers

##taille de chaque cluster
cl$size



