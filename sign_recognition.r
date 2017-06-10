library(pixmap)
library(stringi)

path = "/Users/arnevonberg/Documents/Image_Recognition/GTSRB/Final_Training/Images/"
class = "00022"
overview_csv <- function (class){
  file = paste(path, class, "/GT-", class, ".csv", sep ="")
  read.csv(file, header = TRUE, sep = ";")
}

create.vector <- function (class, filename, grey = TRUE){
  if(grey){
    filename = paste(substr(filename,1,stri_length(filename)-4), ".pgm", sep="")
  }
  image <- read.pnm(paste(path, class,"/grey/", filename, sep=""))
  #plot(image)
  res <- getChannels(image)
  dim(res) <- NULL
  res
}

create.matrix <- function (class, files, grey = TRUE){
  mat = c()
  for(i in 1:nrow(files)){
    mat = c(mat,create.vector(class, files["Filename"][i,], grey=grey))
  }
  matrix(mat, ncol=length(files["Filename"][,1]), nrow=length(mat)
         / length(files["Filename"][,1]))
}

plot.vectorImage <- function(vec){
  b = pixmapGrey(data=vec,nrow=40,ncol=40)
  plot(b)
}

files = overview_csv(class)
a <- create.matrix(class, files, grey=TRUE)
plot.vectorImage(rowMeans(a))

