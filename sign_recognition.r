install.packages("e1071")
install.packages("gmum.r")


library(pixmap)
library(stringi)
library(class)
library(e1071)
library(gmum.r)
path = "/Users/Tobi/git/Image_Recognition/GTSRB/Final_Training/Images/"
classes= c("00000","00001","00002","00003","00004","00005", "00007", "00008")

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
  #TODO Preprocessing folder anpassen
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
  rightKNN = rightSVM = 0;
  for(i in 1:length(samples)){
    train_data = c()
    train_cl = c()
    test_data = samples[[i]]$data
    test_cl = samples[[i]]$class
    
    for(j in 1:length(samples)){
      if(i != j){
        tmp = samples[[j]]
        train_data = cbind(train_data, tmp$data)
        train_cl = c(train_cl, tmp$class)
      }
    }
    print(paste("Group", i, "of", length(samples), "is being tested"))
    
    classificationKNN <- knn(t(train_data), t(test_data), train_cl, k=3)
    total = total + length(classificationKNN)
    rightKNN = rightKNN + sum(classificationKNN == test_cl) 
    print("Finished KNN for this group")
    
    d = data.frame("Data"=t(train_data), "Class"=train_cl)
    model <- svm(Class ~ ., data = d, cost = 100, gamma = 1)
    classificationSVM <- predict(model, t(test_data))
    rightSVM = rightSVM + sum(classificationSVM == test_cl)
    print("Finished SVM for this group")
  }
  print(paste(rightKNN, "out of", total, "signs were classified right by KNN"))
  print(paste(rightSVM, "out of", total, "signs were classified right by SVM"))
}



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
testFeatures
#plot(x=testFeatures[,"loc_48_1241745_11_4916518head_2519.pgm"], y=testFeatures[c(1:1600),])
classificationKNN <- knn(t(a[[1]]), t(testFeatures), a[[2]], k=3)
classificationKNN


##SVM OVA

d = data.frame("Data"=t(a[[1]]), "Class"=a[[2]])

#one vs all
sv.ova <- SVM(Class ~ ., data=d, class.type="one.versus.all", verbosity=0)
preds.ova <- predict(sv.ova, t(testFeatures))

preds.ova
#one vs one
sv.ovo <- SVM(Class ~ ., data=d, class.type="one.versus.one", verbosity=0)
preds.ovo <- predict(sv.ovo, t(testFeatures))

preds.ovo



#SVM OVO (default package)

model <- svm(Class ~ ., data = d, cost = 100, gamma = 1)
classificationSVM <- predict(model, t(testFeatures))
classificationSVM #HOLY MOLY dauert das bei einem bild (okay, 12000 train daten) ewig?!?! wegen one vs. one?
#-> http://r.gmum.net/samples/svm.multiclass.html als alternative?



#evaluate performance on training data based on k-fold cross validation

a <- combinedData(classes, grey=TRUE)
b <- create.samplegroups(a[[1]], a[[2]],600)
c <- pattern.recognition(b)
