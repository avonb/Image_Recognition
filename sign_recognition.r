install.packages("e1071")
install.packages("gmum.r")


library(pixmap)
library(stringi)
library(class)
library(e1071)

library(nnet)
path = "/Users/arnevonberg/Documents/Image_Recognition/GTSRB/Final_Training/Images/"
classes= c("00001","00002", "00004","00007")

#Creates data frame from overview csv
loadClassCSV <- function (class){
  file = paste(path, class, "/GT-", class, ".csv", sep ="")
  read.csv(file, header = TRUE, sep = ";")
}

#Creates vector from image
create.vector <- function (class, filename, grey = TRUE){
  if(grey){
    #Monochromatic images have different file type
    filename = paste(substr(filename,1,stri_length(filename)-4), ".pgm", sep="")
  }
  image <- read.pnm(paste(path, class,"/grey/", filename, sep=""))
  res <- getChannels(image)
  dim(res) <- NULL
  res
}

#Creates matrix from all images
create.matrix <- function (class, grey = TRUE){
  files <- loadClassCSV(class)
  mat = c()
  for(i in 1:nrow(files)){
    mat = c(mat,create.vector(class, files["Filename"][i,], grey=grey))
  }
  matrix(mat, ncol=length(files["Filename"][,1]), nrow=length(mat)
         / length(files["Filename"][,1]))
}

#combines data from all class into one data frame with classification 
combinedData <- function (classes, grey = TRUE){
  data = c()
  #Classification of items
  cl = c()
  for(i in 1:length(classes)){
    mat <- create.matrix(classes[i], grey=grey)
    cl = c(cl, rep(classes[i], dim(mat)[2]))
    data <- cbind(data,mat)
  }
  res = list("data"=data, "classification" = cl)
  res
}

# total number of samples has to be dividable by size
create.samplegroups <- function(data, cl, size){
  n = length(cl)
  perm = sample(c(1:n), replace = FALSE)
  res = list()
  # creates and saves permutation
  for(i in 0:floor(n/size-1)){
    upper = i * size + 1
    lower = i * size + size
    res[[i + 1]] <- list("data" = data[,perm[lower:upper]], 
                         "class" = cl[perm[lower:upper]])
  }
  res
}

#Plots image from vector
plot.vectorImage <- function(vec){
  b = pixmapGrey(data=vec,nrow=40,ncol=40)
  plot(b)
}

#Runs classification algorithms
pattern.recognition <- function(samples){
  reslist = list()
  total = 0;
  rightKNN = rightSVM = rightANN = rightNN = 0;
  
  #Creates training groups
  for(i in 1:length(samples)){
    train_data = c()
    train_cl = c()
    test_data = samples[[i]]$data
    test_cl = samples[[i]]$class
    #Combines data
    for(j in 1:length(samples)){
      if(i != j){
        tmp = samples[[j]]
        train_data = cbind(train_data, tmp$data)
        train_cl = c(train_cl, tmp$class)
      }
    }
    print(paste("Group", i, "of", length(samples), "is being tested"))
    
    #Run KNN
    classificationKNN <- knn(t(train_data), t(test_data), train_cl, k=3)
    total = total + length(classificationKNN)
    rightKNN = rightKNN + sum(classificationKNN == test_cl) 
    print(paste("Finished KNN for this group.", rightKNN ,"/", total))
    
    #Run KNN again, with k = 1
    classificationNN <- knn(t(train_data), t(test_data), train_cl, k=1)
    rightNN = rightNN + sum(classificationKNN == test_cl) 
    print(paste("Finished KNN for this group.", rightNN ,"/", total))
    
    #Run ANN
    targets <- class.ind(train_cl)
    netz <- nnet(t(train_data), targets, size = 4, rang = 0.5, 
                 decay = 1, maxit = 200, MaxNWts = 5000)
    rightANN = rightANN + 
      sum(class.ind(test_cl) == round(predict(netz, t(test_data))))/2
    print(paste("Finished ANN for this group.", rightANN ,"/", total))
    
    #Run SVM
    d = data.frame("Data"=t(train_data), "Class"=train_cl)
    model <- svm(Class ~ ., data = d, cost = 100, gamma = 1, kernel="polynomial")
    classificationSVM <- predict(model, t(test_data))
    rightSVM = rightSVM + sum(classificationSVM == test_cl)
    print(paste("Finished SVM for this group.", rightSVM ,"/", total))
  }
  print(paste(rightKNN, "out of", total, "signs were classified right by KNN"))
  print(paste(rightNN, "out of", total, "signs were classified right by NN"))
  print(paste(rightANN, "out of", total, "signs were classified right by ANN"))
  print(paste(rightSVM, "out of", total, "signs were classified right by SVM"))
}



#Main Block for pattern recognition 
##### RUN THIS ####
a <- combinedData(classes, grey=TRUE)
b <- create.samplegroups(a[[1]], a[[2]],600)
c <- pattern.recognition(b)




###################################################################
#####                                                         #####
#####               Google Streetview Extension               #####
#####                                                         #####
###################################################################

#repeat if necessary
a <- combinedData(classes, grey=TRUE)

crawledImgPath = "/Users/Tobi/git/Image_Recognition/crawledImages/grey"

crawledImgs <- list.files(path = crawledImgPath)

testFeatures = sapply(crawledImgs, function(x) {
                        img = read.pnm(paste(crawledImgPath, x, sep="/"))
                        testedFeatures <- getChannels(img)
                        dim(testedFeatures) <- NULL
                        testedFeatures
                })

classificationKNN <- knn(t(a[[1]]), t(testFeatures), a[[2]], k=3)
classificationKNN




#SVM OVO (default package)

model <- svm(Class ~ ., data = d, cost = 100, gamma = 1)
classificationSVM <- predict(model, t(testFeatures))
classificationSVM




