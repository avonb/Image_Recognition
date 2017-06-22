library(pixmap)
library(stringi)
library(class)

path = "/Users/arnevonberg/Documents/Image_Recognition/GTSRB/Final_Training/Images/"
class = "00000"

overview_csv <- function (class){
  file = paste(path, class, "/GT-", class, ".csv", sep ="")
  read.csv(file, header = TRUE, sep = ";")
}

create.vector <- function (class, filename, grey = TRUE){
  if(grey){
    filename = paste(substr(filename,1,stri_length(filename)-4), ".pgm", sep="")
  }
  image <- read.pnm(paste(path, class,"/grey/", filename, sep=""))
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

patter.recognition <- function(class1, class2, method, test=""){
  files1 <- overview_csv(class1)
  files2 <- overview_csv(class2)
  a <- create.matrix(class1, files1, grey=TRUE)
  b <- create.matrix(class2, files2, grey=TRUE)
  if(method == "knn"){
    sample1 <- sample(1:length(a[1,]),dim(a)[2],replace = FALSE)
    sample2 <- sample(1:length(b[1,]),dim(b)[2],replace = FALSE)
    train <- cbind(a[,sample1[1:floor(length(sample1)*0.9)]], 
                   b[,sample2[1:floor(length(sample2)*0.9)]])
    test <- cbind(a[,sample1[floor(length(sample1)*0.9+1):length(sample1)]], 
                  b[,sample2[floor(length(sample2)*0.9+1):length(sample2)]])
    cl <- factor(c(rep(class1, floor(length(sample1)*0.9)),
                   rep(class2, floor(length(sample2)*0.9))))
    knn(t(train), t(test), cl, k=3, prob=TRUE)
  }
}

files = overview_csv(class)
a <- create.matrix(class, files, grey=TRUE)
plot.vectorImage(rowMeans(a))

